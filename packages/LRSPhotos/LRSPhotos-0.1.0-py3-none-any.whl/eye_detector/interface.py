#!/usr/bin/env python3

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib.request


class EyeDetectorInterface:

    def __init__(self, param_path):
        self.param_path = param_path
        self.model = cv2.ml.SVM_load(param_path)

    @staticmethod
    def create(folder):

        if not os.path.isdir(folder):
            print('Creating new folder to download params into')
            os.makedirs(folder)

        param_path = os.path.join(folder, 'svm_data.xml')

        if not os.path.isfile(param_path) or not os.access(param_path, os.R_OK):
            print('Downloading parameters to path:', os.path.abspath(param_path))
            url = 'https://storage.googleapis.com/cv_final/model_dir/svm_data.xml'
            urllib.request.urlretrieve(url, param_path)
            print('Finished')
            pass

        return EyeDetectorInterface(param_path)

    # Stores hog value of img into data[data_idx, :] and label into labels[data_idx, 0]
    def get_hog(self, img, data_idx, data, label, labels):
        winSize = (40,40)
        blockSize = (16,16)
        blockStride = (8,8)
        cellSize = (8,8)
        nbins = 16
        derivAperture = 1
        winSigma = 4.
        histogramNormType = 0
        L2HysThreshold = 2.0000000000000001e-01
        gammaCorrection = 0
        nlevels = 64

        hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
                                histogramNormType,L2HysThreshold,gammaCorrection,nlevels)
        hog_val = hog.compute(img)
        data[data_idx, :] = hog_val.reshape(1024,)
        labels[data_idx, 0] = label
        data_idx += 1
        return data_idx

    def check_border(self, coor, img0_x, img0_y, dist):
        if (coor[0] < dist or coor[1] < dist):
            return True
        elif (coor[1] > (img0_x - dist) or coor[0] > (img0_y - dist)):
            return True
        return False

    def get_range(self, coor, dist):
        x_low = coor[1] - dist
        x_high = coor[1] + dist
        y_low = coor[0] - dist
        y_high = coor[0] + dist
        return x_low, x_high, y_low, y_high

    def preprocess_bioid(self, bioid_path, patch_diameter):
        img0 = cv2.imread(bioid_path + 'BioID_0020.pgm', cv2.IMREAD_GRAYSCALE)
        pos_data0 = open(bioid_path + "BioID_0020.eye", "r")
        lx, ly, rx, ry = (pos_data0.read()[13:]).split('\t')

        # Pre-process all BioID Face data
        pos_data = [] # stores all positive image patches
        neg_data = [] # stores all negative image patches

        neg_offset = patch_diameter
        dist = patch_diameter // 2
        img0_x, img0_y = img0.shape
        x = np.arange(img0_x)
        y = np.arange(img0_y)
        xx, yy = np.meshgrid(x, y)
        coors = np.concatenate([xx.reshape(-1,1), yy.reshape(-1, 1)], 1)

        data = np.zeros([15200, 1024]) # now oversized
        data_idx = 0
        labels = np.zeros([15200, 1])

        for i in range(1520):
            sample_pgm = bioid_path + 'BioID_' + str(i).zfill(4) + '.pgm'
            sample_eye = bioid_path + 'BioID_' + str(i).zfill(4) + '.eye'
            img = cv2.imread(sample_pgm, cv2.IMREAD_GRAYSCALE)
            
            pos_sample = open(sample_eye, "r")
            lx, ly, rx, ry = (pos_sample.read()[13:]).split('\t')
            left_eye = np.array([int(lx), int(ly)])
            right_eye = np.array([int(rx), int(ry)])
            
            # append left eye
            if not self.check_border(left_eye, img0_x, img0_y, dist):
                x_low, x_high, y_low, y_high = self.get_range(left_eye, dist)
                patch = cv2.resize(img[x_low:x_high, y_low:y_high], (40, 40))
                pos_data.append(patch)
                data_idx = self.get_hog(pos_data[-1], data_idx, data, 1, labels)
            # append right eye
            if not self.check_border(right_eye, img0_x, img0_y, dist):
                x_low, x_high, y_low, y_high = self.get_range(right_eye, dist)
                patch = cv2.resize(img[x_low:x_high, y_low:y_high], (40, 40))
                pos_data.append(patch)
                data_idx = self.get_hog(pos_data[-1], data_idx, data, 1, labels)
            
            # sample first, then check if within eye regions
            neg_idx = np.random.randint(0,coors.shape[0],size=3)
            for idx in neg_idx:
                neg_sample = coors[idx]
                # check if within eye regions
                if (left_eye[0] - neg_offset < neg_sample[0] < right_eye[0] + neg_offset) and (left_eye[1] - neg_offset < neg_sample[1] < right_eye[1] + neg_offset):
                    continue
                # check if within border regions
                elif not self.check_border(neg_sample, img0_x, img0_y, dist):
                    x_low, x_high, y_low, y_high = self.get_range(neg_sample, dist)
                    patch = cv2.resize(img[x_low:x_high, y_low:y_high], (40, 40))
                    neg_data.append(patch)
                    data_idx = self.get_hog(neg_data[-1], data_idx, data, -1, labels)
        return pos_data, neg_data, data[:data_idx,:], labels[:data_idx,:]

    # Helper to split data into 9 training folds and 1 testing fold
    def split_bioid(self, pos_data, neg_data, data, labels):
        # Split data for training and testing
        total_data = len(pos_data) + len(neg_data)
        test_total = total_data // 10 # 1/10 for testing

        # Create dictionary to store 10 different splits
        data_dict = {'train_data':[],'test_data':[], 'train_labels':[], 'test_labels':[]}
        for i in range(10):
            data_dict['test_data'].append(data[(i * test_total):((i + 1) * test_total), :])
            data_dict['test_labels'].append(labels[(i * test_total):((i + 1) * test_total), :])
            train_data0 = data[0:(i * test_total), :].reshape(-1, 1024)
            train_data1 = data[((i + 1) * test_total):total_data, :].reshape(-1, 1024)
            train_labels0 = labels[0:(i * test_total), :].reshape(-1, 1)
            train_labels1 = labels[((i + 1) * test_total):total_data, :].reshape(-1, 1)
            data_dict['train_data'].append(np.concatenate((train_data0, train_data1), axis = 0))
            data_dict['train_labels'].append(np.concatenate((train_labels0, train_labels1), axis = 0))
        return data_dict

    # bioid path is where the BioID images are stored
    def train(self, bioid_path):
        if (bioid_path[-1] != '/'):
            bioid_path = bioid_path + '/'
        _, _, data, labels = self.preprocess_bioid(bioid_path)

        # Set training parameters
        svm = cv2.ml.SVM_create()
        svm.setKernel(cv2.ml.SVM_LINEAR)
        svm.setType(cv2.ml.SVM_C_SVC)
        svm.setC(0.7) # soft margin previously 2.67
        svm.setGamma(6) # radial basis function previously 5.383

        svm.train(data.astype(np.float32), cv2.ml.ROW_SAMPLE, labels.astype(np.int32))
        svm.save('svm_data.xml')

    # Test overall detection model
    def test(self, bioid_path):
        svm = cv2.ml.SVM_create()
        svm.setKernel(cv2.ml.SVM_LINEAR)
        svm.setType(cv2.ml.SVM_C_SVC)
        svm.setC(0.7) # soft margin previously 2.67
        svm.setGamma(6) # radial basis function previously 5.383
        
        pos_data, neg_data, data, labels = self.preprocess_bioid(bioid_path)
        total_data = len(pos_data) + len(neg_data)
        test_total = total_data // 10 # 1/10 for testing
        data_dict = self.split_bioid(pos_data, neg_data, data, labels)

        accuracies = []
        for i in range(10):
            train_data = data_dict['train_data'][i]
            test_data = data_dict['test_data'][i]
            train_labels = data_dict['train_labels'][i]
            test_labels = data_dict['test_labels'][i]
            svm.train(train_data.astype(np.float32), cv2.ml.ROW_SAMPLE, train_labels.astype(np.int32))
            svm.save('svm_data.xml')
            results = np.zeros([test_total, 1])
            for i in range(test_total):
                results[i, 0] = svm.predict(test_data[i,:].reshape(1,-1).astype(np.float32))[1]

            mask = results==test_labels
            correct = np.count_nonzero(mask)
            accuracies.append(correct / test_total)
            print(accuracies[-1])

    # Cross validation on binary classification model (SVM)
    def train_and_test(self, bioid_path, scales=[40]):
        # Set training parameters
        svm = cv2.ml.SVM_create()
        svm.setKernel(cv2.ml.SVM_LINEAR)
        svm.setType(cv2.ml.SVM_C_SVC)
        svm.setC(0.7) # soft margin previously 2.67
        svm.setGamma(6) # radial basis function previously 5.383
        
        if (len(scales) == 0):
            print("Must choose at least one scale!! If you don't know where to start, leave this parameter empty.")
            return

        pos_data, neg_data, data, labels = self.preprocess_bioid(bioid_path, scales[0])
        if (len(scales) > 1):
            for scale in scales[1:]:
                new_pos_data, new_neg_data, new_data, new_labels = self.preprocess_bioid(bioid_path, scale)
                pos_data = pos_data + new_pos_data
                neg_data = neg_data + new_neg_data
                data = np.vstack((data, new_data))
                labels = np.vstack((labels, new_labels))

        total_data = len(pos_data) + len(neg_data)
        test_total = total_data // 10 # 1/10 for testing
        data_dict = self.split_bioid(pos_data, neg_data, data, labels)

        accuracies = []
        for i in range(10):
            train_data = data_dict['train_data'][i]
            test_data = data_dict['test_data'][i]
            train_labels = data_dict['train_labels'][i]
            test_labels = data_dict['test_labels'][i]
            svm.train(train_data.astype(np.float32), cv2.ml.ROW_SAMPLE, train_labels.astype(np.int32))
            svm.save('svm_data.xml')
            results = np.zeros([test_total, 1])
            for i in range(test_total):
                results[i, 0] = svm.predict(test_data[i,:].reshape(1,-1).astype(np.float32))[1]

            mask = results==test_labels
            correct = np.count_nonzero(mask)
            accuracies.append(correct / test_total)
            print(accuracies[-1])
   

   # Sequential Labeling Algorithm to segment the coordinates
    def seq_labeling(self, y_coords, x_coords, stride):
        labeled = {} # coor: label
        equivalence = [] # a list of equivalence sets
        offsets = np.array([[-stride,-stride],[0,-stride],[stride,-stride],
                            [-stride,0],[stride,0],[-stride,stride],
                            [0,stride],[stride,stride]])
        labeled_flag = 0
        num_labels = 0
        for i in range(y_coords.size):
            labeled_flag = 0
            xx = x_coords[i]
            yy = y_coords[i]
            neighbors = (np.array([xx,yy]) + offsets).tolist()
            for n in neighbors:
                nn = (n[0],n[1])
                if labeled_flag == 0:
                    if nn in labeled:
                        labeled[(xx,yy)] = labeled[nn]
                        labeled_flag = 1
                elif nn in labeled: # (xx,yy) already labeled
                    if labeled[nn] != labeled[(xx,yy)]:
                        noted = 0 # flag
                        # note in our list of equivalence sets
                        for e in equivalence:
                            if labeled[nn] in e:
                                e.add(labeled[(xx,yy)])
                                noted = 1
                            elif labeled[(xx,yy)] in e:
                                e.add(labeled[nn])
                                noted = 1
                        if noted == 0:
                            equivalence.append({labeled[nn], labeled[(xx,yy)]})
            
            # if no neighbor has been labeled
            if labeled_flag == 0:
                labeled[(xx,yy)] = num_labels # adds new label
                num_labels+= 1
        
        # one final pass to adjust for equivalencies
        for l in labeled:
            cur_label = labeled[l]
            for e in equivalence:
                if cur_label in e:
                    labeled[l] = np.min(list(e))
        return labeled

    # Finds 2 labels that correspond to the 2 eyes 
    def find_eyes(self, labeled, m):
        labels = {}
        for l in labeled:
            if labeled[l] not in labels:
                labels[labeled[l]] = {l}
            else:
                labels[labeled[l]].add(l)
        
        ind_scores = {} # evaluate each label individually
        centers = {}
        for l in labels:
            y_average = np.sum(np.array(list(labels[l]))[:,1]) / np.array(list(labels[l])).shape[0]
            x_average = np.sum(np.array(list(labels[l]))[:,0]) / np.array(list(labels[l])).shape[0]
            centers[l] = np.array([x_average, y_average]).astype(np.int)
            # 1. maximizes number of votes (prioritized)
            # 2. minimizes average y value
            ind_scores[l] = len(labels[l]) / (y_average**2)
        
        if (len(labels) < 3):
            return list(centers.values())
        
        # Evaluate all pairs and encourage
        # 1. minimize difference between y values
        # 2. maximize difference between x values
        # 3. maximize the 2's individual scores
        scores = {}
        for l1 in labels:
            for l2 in labels:
                if (l1 == l2):
                    continue
                y_diff = np.abs(centers[l1][1] - centers[l2][1])
                x_diff = np.abs(centers[l1][0] - centers[l2][0])
                if (y_diff == 0):
                    y_diff = 0.01
                scores[(l1, l2)] = ind_scores[l1] * ind_scores[l2] * (x_diff**2) / y_diff
        
        res_labels = sorted(scores, key=scores.get, reverse=True)[0]
        return [centers[res_labels[0]], centers[res_labels[1]]]

    # param_path is the path is where svm_data.xml is stored
    def detect(self, img):
        svm = self.model
        winSize = (40,40)
        blockSize = (16,16)
        blockStride = (8,8)
        cellSize = (8,8)
        nbins = 16
        derivAperture = 1
        winSigma = 4.
        histogramNormType = 0
        L2HysThreshold = 2.0000000000000001e-01
        gammaCorrection = 0
        nlevels = 64

        hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
                                histogramNormType,L2HysThreshold,gammaCorrection,nlevels)
        m, n = img.shape
        
        # for images that are big enough
        step = max(1, n // 90)
        length = step * 20
        stride = 4 # to cut down on computation costs
        
        if (m < 20 or n < 20):
            return None

        if (n < 35):
            length = step * 5
            stride = 1
        elif (n < 50):
            length = step * 7
            stride = 1
        elif (n < 90):
            length = step * 12
            stride = 1
        elif (n < 120):
            length = step * 16
            stride = 2
        
        x_range = length + np.array([stride * n for n in range((m - 2 * length - 2) // stride)])
        y_range = length + np.array([stride * n for n in range((n - 2 * length - 2) // stride)])
        res = np.zeros([m, n])

        for x in x_range:
            for y in y_range:
                sub_img = cv2.resize(img[(x-length):(x+length):step, (y-length):(y+length):step], (40, 40))
                temp = svm.predict(hog.compute(sub_img).astype(np.float32).reshape(1,-1))[1][0][0]
                res[x,y] = 0 if temp == -1 else 1
                
        mask = res>0
        y_coords, x_coords = np.nonzero(mask)
        
        # Call Sequential Labeling function
        labeled = self.seq_labeling(y_coords, x_coords, stride)
        
        # Call method to locate the eyes
        try:
            eyes = self.find_eyes(labeled, m)
            if (len(eyes) == 0):
                return None
            return (eyes, length)
        except:
            return None
