from __future__ import absolute_import


import sys
import argparse

def main():
    parent_parser = argparse.ArgumentParser(description="Deep-Motilidad is developed by several members of the University of La Rioja")

    subparsers = parent_parser.add_subparsers(title='Subcommands',
                                              description='There are 2 supported commands: classification and segmentation',
                                              dest='mode',
                                              help='Additional help')

    # Classification Command
    parser_classification = subparsers.add_parser('classification', help='Classification of a folder with motility images')
    parser_classification.add_argument("input", help='Input folder path (str)', type=str)
    parser_classification.add_argument("output", help='Output folder path (str)', type=str) 

   
    # Folder Command
    parser_segmentation = subparsers.add_parser('segmentation', help='Segmentation of a folder with motility images')
    parser_segmentation.add_argument("input", help='Input folder path (str)', type=str)
    parser_segmentation.add_argument("output", help='Output folder path (str)', type=str)

    # Parsing args
    args = parent_parser.parse_args()

    if args.mode == "classification":
        from .predict_clas import predict_classification
        predict_classification(input_folder=args.input, output_folder=args.output)
    elif args.mode == "segmentation":
        from .predict_seg import predict_segmentation 
        predict_segmentation(input_folder=args.input, output_folder=args.output)
    
    
