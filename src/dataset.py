import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils import *
import argparse

def load_data_json(path, args):
    instructions = []
    labels = []

    set_name = get_name(args)
    dir = 'Create_new_slides' if args.dataset == 'short' else 'Edit_PPT_template'
    read_path = os.path.join(path, set_name, dir)

    for json_file in sorted(os.listdir(read_path),key=lambda x:int(x.split('_')[1].split('.')[0])):
        if json_file.endswith('.json'):
            print(json_file)
            text = open(os.path.join(read_path,json_file)).read()
            jsons = text.split('\n')[:-1]
            instruction = []
            label = []
            for json_line in jsons:
                parsed_data = json.loads(json_line)

                user_instruction = parsed_data['User instruction']
                api_sequence = parsed_data['Feasible API sequence'].strip(';').split(';')

                instruction.append(user_instruction)
                label.append(api_sequence)

            instructions.append(instruction)
            labels.append(label)
    
    return instructions, labels

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # PPT assistant
    parser.add_argument("--data_path", default="test", type=str,
                        help="The data path to load the instructions")
    parser.add_argument("--dataset", default="short", type=str,
                        help="short/long")
    parser.add_argument("--model_id", default="None", type=str,
                        help="short/long")
    parser.add_argument("--user_path", default='PPTCR/PPTCR_test_input', type=str,
                        help="the user storage file path ")
    parser.add_argument("--save_path", default="test_pptx_data", type=str,
                        help="the path to save the intermediate ppts.")
    
    # mode
    parser.add_argument("--prepare", default=False, action='store_true',
                        help='whether to prepare the data for the model')
    parser.add_argument("--eval", default=False, action='store_true',
                        help='whether to evaluate the pptx file generated by the model')
    parser.add_argument("--test", default=False, action='store_true',
                        help='whether to test on the instruction data loaded from data_path')
    parser.add_argument("--tf", default=False, action='store_true',
                        help='whether to use teacher forcing mode')
    parser.add_argument("--sess", default=False, action='store_true',
                        help='whether to test from session level')
    parser.add_argument("--resume", default=False, action='store_true',
                        help='whether to continue generation from the last unfinished instruction')
    
    # modeling
    parser.add_argument("--model", default="turbo",type=str,
                        help="turbo/gpt4/text3") 
    parser.add_argument("--planning", default=False, action='store_true',
                        help="whether to apply the planning module") 
    parser.add_argument("--api_selection", default=False, action='store_true',
                        help="whether to apply the api selection module") 
    parser.add_argument("--api_topk", default=10, type=int,
                        help="How many apis to retrieve from the api pool") 
    parser.add_argument("--content_selection", default=False, action='store_true',
                        help="whether to apply the shape selection module") 
    
    # api update/lack
    parser.add_argument("--api_lack", default=False, action='store_true',
                        help='whether to test in the api lack setting')
    parser.add_argument("--api_update", default=False, action='store_true',
                        help='whether to test in the api update setting')
    parser.add_argument("--second", default=False, action='store_true',
                        help='second test')

    parser.add_argument("--robust", default=False, action='store_true',
                        help='whether to test in robust data')
    parser.add_argument("--robust_num", default=0, type=int,
                        help="which robusted data") 
    parser.add_argument("--noisy", default=False, action='store_true',
                        help='whether to test in noisy data')
    parser.add_argument("--language", default="English", type=str,
                        help='which language')

    args = parser.parse_args()

    instructions1, labels1 = load_data_json(args.user_path, args)