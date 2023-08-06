import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from torch.nn.functional import softmax
from tfkit.model.oncectc.dataloader import get_feature_from_data
from tfkit.utility.loss import *
from tfkit.utility.tok import *
from tfkit.utility.loss import SeqCTCLoss


class Model(nn.Module):
    def __init__(self, tokenizer, pretrained, maxlen=512, tasks_detail=None):
        super().__init__()
        self.tokenizer = tokenizer
        self.pretrained = pretrained
        self.maxlen = maxlen
        self.loss = SeqCTCLoss()
        self.model = nn.Linear(self.pretrained.config.hidden_size, self.tokenizer.__len__())
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print('Using device:', self.device)
        self.model.to(self.device)

    def forward(self, batch_data, eval=False):
        inputs = batch_data['input']
        targets = batch_data['target']
        targets_nopad = batch_data['target_nopad']
        masks = batch_data['mask']
        types = batch_data['type']
        starts = batch_data['start']
        lengths = batch_data['length']

        tokens_tensor = torch.as_tensor(inputs).to(self.device)
        mask_tensors = torch.as_tensor(masks).to(self.device)
        type_tensors = torch.as_tensor(types).to(self.device)
        loss_tensors = torch.as_tensor(targets_nopad).to(self.device)
        length_tensors = torch.as_tensor(lengths).to(self.device)
        start_tensors = torch.as_tensor(starts).to(self.device)

        output = self.pretrained(tokens_tensor, attention_mask=mask_tensors)
        sequence_output = output[0]
        prediction_scores = self.model(sequence_output)

        batch_size = list(tokens_tensor.shape)[0]
        prediction_scores = prediction_scores.view(batch_size, -1, self.pretrained.config.vocab_size)
        if eval:
            pscore = prediction_scores.detach().cpu()
            result_dict = {
                'label_prob_all': [],
                'label_map': [],
                'prob_list': []
            }
            start = 0
            outputs = result_dict
            while start < self.maxlen:
                predicted_index = torch.argmax(pscore[0][start]).item()
                predicted_token = self.tokenizer.decode([predicted_index])
                logit_prob = softmax(prediction_scores[0][start], dim=0).data.tolist()
                prob_result = {self.tokenizer.decode([id]): prob for id, prob in enumerate(logit_prob)}
                prob_result = sorted(prob_result.items(), key=lambda x: x[1], reverse=True)
                if tok_sep(self.tokenizer) == predicted_token:
                    break
                result_dict['prob_list'].append(sorted(logit_prob, reverse=True))
                result_dict['label_prob_all'].append(dict(prob_result))
                result_dict['label_map'].append(prob_result[0])
                start += 1
                outputs = result_dict
        else:
            masked_lm_loss = self.loss(prediction_scores,
                                       type_tensors,
                                       loss_tensors.view(batch_size, -1),
                                       length_tensors)
            outputs = masked_lm_loss

        return outputs

    def predict(self, input='', task=None, handle_exceed='start_slice'):
        handle_exceed = handle_exceed[0] if isinstance(handle_exceed, list) else handle_exceed
        self.eval()
        with torch.no_grad():
            ret_result = []
            ret_detail = []
            feature = get_feature_from_data(self.tokenizer, self.maxlen, input, handle_exceed=handle_exceed)[-1]
            for k, v in feature.items():
                feature[k] = [v]
            predictions = self.forward(feature, eval=True)
            output = "".join(self.tokenizer.convert_tokens_to_string([i[0] for i in predictions['label_map']]))
            ret_result.append(output)
            ret_detail.append(predictions)
            return ret_result, ret_detail
