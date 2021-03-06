'''
Author      : now more
Contact     : lin.honghui@qq.com
LastEditors: Please set LastEditors
LastEditTime: 2020-10-31 22:31:36
Description : 
'''
# from .build import FullModel
import copy
import torch
import model.net as Net

def build_model(cfg,pretrain_path=""):
    cfg = copy.deepcopy(cfg)
    if 'net' in cfg['model'].keys():
        net_cfg = cfg['model']['net']
        net_type = net_cfg.pop("type")
        model = getattr(Net,net_type)(cfg)
    else:
        raise KeyError("`net` not in cfg['model']")
    if pretrain_path:
        model_state_dict = model.state_dict()
        state_dict = torch.load(pretrain_path,map_location='cpu')
        if 'model' in state_dict.keys():
            state_dict = state_dict['model']
        for key in state_dict.keys():
            if key in model_state_dict.keys() and state_dict[key].shape==model_state_dict[key].shape:
                # print("perfect")
                model_state_dict[key] = state_dict[key]
        model.load_state_dict(model_state_dict)
    return model
    