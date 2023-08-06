import os

from PIL import Image

import numpy as np
import torch

from phobos.metrics import Metrics


class Logger():
    def __init__(self,
                 image_loader,
                 args,
                 polyaxon_exp=None):
        self.args = args
        self.polyaxon_exp = polyaxon_exp
        self.image_loader = image_loader

    def _patchify(self, image):
        patches, locs = [], []
        w = self.args.input_shape[2]
        for i in range(0, image.shape[2], w):
            for j in range(0, image.shape[3], w):
                if i + w <= image.shape[2] and j + w <= image.shape[3]:
                   patches.append(image[:, :, i:i+w, j:j+w])
                   locs.append([i, j])
        return np.asarray(patches), locs

    def _unpatchify(self, patches, locs, shape):
        output = np.zeros((shape[0], shape[1]))
        w = self.args.input_shape[2]
        for i in range(len(locs)):
            x, y = locs[i]
            output[x:x+w, y:y+w] = patches[i]

        return (output * 255).astype(np.uint8)

    def predict_and_log(self, model, epoch):
        model.eval()
        for image_path in self.args.images_to_be_logged:
            image = self.image_loader(os.path.join(self.args.dataset_dir,
                                                   image_path))
            shape = [image.shape[2], image.shape[3]]
            patches, locs = self._patchify(image)

            result = []
            for i in range(0, len(patches), self.args.batch_size):
                batch = torch.tensor(patches[i:i+self.args.batch_size])
                if self.args.gpu > -1:
                    batch = batch.to(self.args.gpu)
                preds = model(batch)
                preds = Metrics._argmax_or_thresholding(preds).numpy()
                result.append(preds.astype(np.uint8))

            result = np.concatenate(result)

            pred_mask = self._unpatchify(result, locs, shape)

            if self.polyaxon_exp:
                self.polyaxon_exp.log_image(data=pred_mask,
                                            name=image_path.replace('/', '_'),
                                            step=epoch)

            im = Image.fromarray(pred_mask)
            im.save(os.path.join(self.args.log_dir,
                    'epoch_' + str(epoch) +  '_' + image_path.replace('/', '_')))
