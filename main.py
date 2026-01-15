#!/usr/bin/env python3

import argparse
import os
import csv
import json
from tasks_runner import TaskRunner

def readargs(args=None):
    parser = argparse.ArgumentParser(
        prog='Text Analyzer project',
    )
    # General arguments
    parser.add_argument('-t', '--task',
                        help="task number",
                        required=True
                        )
    parser.add_argument('-s', '--sentences',
                        help="Sentence file path",
                        )
    parser.add_argument('-n', '--names',
                        help="Names file path",
                        )
    parser.add_argument('-r', '--removewords',
                        help="Words to remove file path",
                        )
    parser.add_argument('-p', '--preprocessed',
                        help="json with preprocessed data",
                        )
    # Task specific arguments
    parser.add_argument('--maxk',
                        type=int,
                        help="Max k",
                        )
    parser.add_argument('--fixed_length',
                        type=int,
                        help="fixed length to find",
                        )
    parser.add_argument('--windowsize',
                        type=int,
                        help="Window size",
                        )
    parser.add_argument('--pairs',
                        help="json file with list of pairs",
                        )
    parser.add_argument('--threshold',
                        type=int,
                        help="graph connection threshold",
                        )
    parser.add_argument('--maximal_distance',
                        type=int,
                        help="maximal distance between nodes in graph",
                        )

    parser.add_argument('--qsek_query_path',
                        help="json file with query path",
                        )
    return parser.parse_args(args)




def main():

    args=readargs()

    if args.task == '1':
        if valid_task_1_arguments(args.sentences, args.names, args.removewords):
            task_runner = TaskRunner()
            task_1_reuslt = task_runner.run_task_1(args.sentences, args.names, args.removewords)
            print(task_1_reuslt)
    
    elif args.task == '2':
        if valid_task_2_arguments(args.preprocessed, args.sentences, args.removewords, args.maxk):
            preprocessed_flow_flag = args.preprocessed != None
            task_runner = TaskRunner(preprocessed_flow_flag, args.preprocessed)
            task_2_reuslt = task_runner.run_task_2(args.sentences, args.removewords, args.maxk)
            print(task_2_reuslt)


    elif args.task == '3':
        if valid_task_3_arguments(args.preprocessed, args.sentences, args.names, args.removewords):
            preprocessed_flow_flag = args.preprocessed != None
            task_runner = TaskRunner(preprocessed_flow_flag, args.preprocessed)
            task_3_reuslt = task_runner.run_task_3(args.sentences, args.names, args.removewords)
            print(task_3_reuslt)

    
    elif args.task == '4':
        if valid_task_4_arguments(args.preprocessed, args.sentences, args.removewords, args.qsek_query_path):
            preprocessed_flow_flag = args.preprocessed != None
            task_runner = TaskRunner(preprocessed_flow_flag, args.preprocessed)
            task_4_reuslt = task_runner.run_task_4(args.sentences, args.removewords, args.qsek_query_path)
            print(task_4_reuslt)

    
    elif args.task == '5':
        if valid_task_5_arguments(args.preprocessed, args.sentences, args.names, args.removewords, args.maxk):
            preprocessed_flow_flag = args.preprocessed != None
            task_runner = TaskRunner(preprocessed_flow_flag, args.preprocessed)
            task_5_reuslt = task_runner.run_task_5(args.sentences, args.names, args.removewords, args.maxk)
            print(task_5_reuslt)

    
    elif args.task == '6':
        if valid_task_6_arguments(args.preprocessed, args.sentences, args.names, args.removewords, args.windowsize, args.threshold):
            preprocessed_flow_flag = args.preprocessed != None
            task_runner = TaskRunner(preprocessed_flow_flag, args.preprocessed)
            task_6_reuslt = task_runner.run_task_6(args.sentences, args.names, args.removewords, args.windowsize, args.threshold)
            print(task_6_reuslt)

    
    elif args.task == '7':
        if valid_task_7_arguments(args.preprocessed, args.sentences, args.names, args.removewords, args.windowsize, args.threshold, args.pairs, args.maximal_distance):
            preprocessed_flow_flag = args.preprocessed != None
            task_runner = TaskRunner(preprocessed_flow_flag, args.preprocessed)
            task_7_reuslt = task_runner.run_task_7(args.sentences, args.names, args.removewords, args.windowsize, args.threshold, args.pairs, args.maximal_distance)
            print(task_7_reuslt)


    elif args.task == '8':
        if valid_task_8_arguments(args.preprocessed, args.sentences, args.names, args.removewords, args.windowsize, args.threshold, args.pairs, args.fixed_length):
            preprocessed_flow_flag = args.preprocessed != None
            task_runner = TaskRunner(preprocessed_flow_flag, args.preprocessed)
            task_8_reuslt = task_runner.run_task_8(args.sentences, args.names, args.removewords, args.windowsize, args.threshold, args.pairs, args.fixed_length)
            print(task_8_reuslt)


    elif args.task == '9':
        if valid_task_9_arguments(args.preprocessed, args.sentences, args.removewords, args.threshold):
            preprocessed_flow_flag = args.preprocessed != None
            task_runner = TaskRunner(preprocessed_flow_flag, args.preprocessed)
            task_9_reuslt = task_runner.run_task_9(args.sentences, args.removewords, args.threshold)
            print(task_9_reuslt)
    
    else:
        print("invalid input: No valid task number provided.")




#
# VALIDATE COMMAND LINE ARGUMETS:
# 

def valid_task_1_arguments(sentences_path: str, names_path: str, remove_words_path: str) -> bool:
    # For Task 1, we expect only CSV paths for sentences, names, and remove words
    if not sentences_path or not names_path or not remove_words_path:
        print("invalid input: One or more paths (sentences, names, or remove words) are missing.")
        return False
        
    if not is_valid_csv_path(sentences_path) or not is_valid_csv_path(names_path) or not is_valid_csv_path(remove_words_path):
        print("invalid input: One or more of the paths (sentences, names, or remove words) are invalid.")
        return False
    
    return True


def valid_task_2_arguments(preprocessed_path: str, sentences_path: str, remove_words_path: str, maximal_kseq: int) -> bool:
    # Task 3 should have either valid preprocessed data with valid maximal_kseq or CSV paths for sentences, remove wordswith valid maximal_kseq
    if preprocessed_path is not None:
        if is_valid_json_path(preprocessed_path) and isinstance(maximal_kseq, int) and maximal_kseq > 0:
            return True
        else:
            print("invalid input: Preprocessed path is invalid or maximal_kseq is not a valid positive integer.")
            return False
    
    # If preprocessed_path doesn't exist, check if sentences_path, remove_words_path, and maximal_kseq are valid
    if sentences_path is not None and remove_words_path is not None:
        if is_valid_csv_path(sentences_path) and is_valid_csv_path(remove_words_path) and isinstance(maximal_kseq, int) and maximal_kseq > 0:
            return True
        else:
            print("invalid input: One or more CSV paths (sentences or remove words) are invalid, or maximal_kseq is not valid.")
            return False
    
    print("invalid input: Missing arguments (sentences or remove words paths) or invalid maximal_kseq.")
    return False


def valid_task_3_arguments(preprocessed_path: str, sentences_path: str, names_path: str, remove_words_path: str) -> bool:
    # Task 3 should have either valid preprocessed data or CSV paths for sentences, names, and remove words
    if preprocessed_path is not None:
        if is_valid_json_path(preprocessed_path):
            return True
        else:
            print("invalid input: Preprocessed path is invalid.")
            return False

    # If no preprocessed data, validate CSV paths for sentences, names, and remove words
    if not sentences_path or not names_path or not remove_words_path:
        print("invalid input: One or more paths (sentences, names, or remove words) are missing.")
        return False
        
    if not is_valid_csv_path(sentences_path) or not is_valid_csv_path(names_path) or not is_valid_csv_path(remove_words_path):
        print("invalid input: One or more of the paths (sentences, names, or remove words) are invalid.")
        return False
    
    return True


def valid_task_4_arguments(preprocessed_path: str, sentences_path: str, remove_words_path: str, kseq_list_path: str) -> bool:
    # Task 4 should have either valid preprocessed data and kseq_list_path or CSV paths with kseq_list_path
    if preprocessed_path is not None and kseq_list_path is not None:
        if is_valid_json_path(preprocessed_path) and is_valid_json_path(kseq_list_path):
            return True
        else:
            print("invalid input: Preprocessed path or kseq_list_path is invalid.")
            return False
        
    # If no preprocessed data, validate CSV paths and kseq_list_path
    if sentences_path is not None and remove_words_path is not None and kseq_list_path is not None:
        if is_valid_csv_path(sentences_path) and is_valid_csv_path(remove_words_path) and is_valid_json_path(kseq_list_path):
            return True
        else:
            print("invalid input: One or more paths (CSV or kseq_list_path) are invalid.")
            return False
    
    print("invalid input: Missing arguments (sentences, remove words, or kseq_list_path).")
    return False


def valid_task_5_arguments(preprocessed_path: str, sentences_path: str, names_path: str, remove_words_path: str, maximal_kseq: int) -> bool:
    # Task 5 should have either valid preprocessed data or CSV paths for sentences, names, and remove words along with maximal_kseq
    if preprocessed_path is not None and isinstance(maximal_kseq, int) and maximal_kseq > 0:
        if is_valid_json_path(preprocessed_path):
            return True
        else:
            print("invalid input: Preprocessed path is invalid or maximal_kseq is not a valid positive integer.")
            return False

    # If no preprocessed data, validate CSV paths for sentences, names, and remove words along with maximal_kseq
    if not sentences_path or not names_path or not remove_words_path or not isinstance(maximal_kseq, int) or maximal_kseq <= 0:
        print("invalid input: One or more arguments (sentences, names, remove words, or maximal_kseq) are missing or invalid.")
        return False
        
    if not is_valid_csv_path(sentences_path) or not is_valid_csv_path(names_path) or not is_valid_csv_path(remove_words_path):
        print("invalid input: One or more CSV paths (sentences, names, or remove words) are invalid.")
        return False
    
    return True


def valid_task_6_arguments(preprocessed_path: str, sentences_path: str, names_path: str, remove_words_path: str, window_size: int, treshold: int) -> bool:
    # Task 6 should have either valid preprocessed data or CSV paths for sentences, names, and remove words along with window_size and treshold
    if preprocessed_path is not None:
        if isinstance(window_size, int) and window_size >= 0 and isinstance(treshold, int) and treshold >= 0:
            if is_valid_json_path(preprocessed_path):
                return True
            else:
                print("invalid input: Preprocessed path is invalid.")
                return False
        else:
            print("invalid input: window_size and/or treshold are invalid.")
            return False

    # If no preprocessed data, validate CSV paths for sentences, names, and remove words, and window_size, treshold
    if sentences_path is not None and names_path is not None and remove_words_path is not None:
        if isinstance(window_size, int) and window_size >= 0 and isinstance(treshold, int) and treshold >= 0:
            if is_valid_csv_path(sentences_path) and is_valid_csv_path(names_path) and is_valid_csv_path(remove_words_path):
                return True
            else:
                print("invalid input: One or more CSV paths are invalid.")
                return False
        else:
            print("invalid input: window_size and/or treshold are invalid.")
            return False
    else:
        print("invalid input: One or more arguments are missing (sentences, names, or remove_words paths).")
        return False


def valid_task_7_arguments(preprocessed_path: str, sentences_path: str, names_path: str, remove_words_path: str, window_size: int, treshold: int, people_connections_json_path: str, maximal_distance: int) -> bool:
    # Task 7 should have either valid preprocessed data, people_connections_json_path, and maximal_distance
    if preprocessed_path is not None and people_connections_json_path is not None and maximal_distance is not None:
        if is_valid_json_path(preprocessed_path) and is_valid_json_path(people_connections_json_path) and isinstance(maximal_distance, int) and maximal_distance >= 0:
            return True
        else:
            print("invalid input: Preprocessed path, people connections JSON, or maximal_distance is invalid.")
            return False

    # If no preprocessed data, validate CSV paths for sentences, names, remove words, window_size, treshold, and other args
    if sentences_path is not None and names_path is not None and remove_words_path is not None and people_connections_json_path is not None:
        if isinstance(window_size, int) and window_size >= 0 and isinstance(treshold, int) and treshold >= 0 and isinstance(maximal_distance, int) and maximal_distance >= 0:
            if is_valid_csv_path(sentences_path) and is_valid_csv_path(names_path) and is_valid_csv_path(remove_words_path) and is_valid_json_path(people_connections_json_path):
                return True
            else:
                print("invalid input: One or more paths are invalid (CSV or JSON).")
                return False
        else:
            print("invalid input: window_size, treshold, or maximal_distance are invalid.")
            return False
    else:
        print("invalid input: One or more arguments are missing (sentences, names, remove_words paths, or people_connections_json_path).")
        return False


def valid_task_8_arguments(preprocessed_path: str, sentences_path: str, names_path: str, remove_words_path: str, window_size: int, treshold: int, people_connections_json_path: str, exact_distance: int) -> bool:
    # Task 8 should have either valid preprocessed data, people_connections_json_path, and exact_distance
    if preprocessed_path is not None and people_connections_json_path is not None and exact_distance is not None:
        if is_valid_json_path(preprocessed_path) and is_valid_json_path(people_connections_json_path) and isinstance(exact_distance, int) and exact_distance >= 0:
            return True
        else:
            print("invalid input: Preprocessed path, people connections JSON, or exact_distance is invalid.")
            return False

    # If no preprocessed data, validate CSV paths for sentences, names, remove words, window_size, treshold, and other args
    if sentences_path is not None and names_path is not None and remove_words_path is not None and people_connections_json_path is not None:
        if isinstance(window_size, int) and window_size >= 0 and isinstance(treshold, int) and treshold >= 0 and isinstance(exact_distance, int) and exact_distance >= 0:
            if is_valid_csv_path(sentences_path) and is_valid_csv_path(names_path) and is_valid_csv_path(remove_words_path) and is_valid_json_path(people_connections_json_path):
                return True
            else:
                print("invalid input: One or more paths are invalid (CSV or JSON).")
                return False
        else:
            print("invalid input: window_size, treshold, or exact_distance are invalid.")
            return False
    else:
        print("invalid input: One or more arguments are missing (sentences, names, remove_words paths, or people_connections_json_path).")
        return False


def valid_task_9_arguments(preprocessed_path: str, sentences_path: str, remove_words_path: str, treshold: int) -> bool:
    # Task 9 should have either valid preprocessed data or CSV paths with treshold
    if preprocessed_path is not None:
        if is_valid_json_path(preprocessed_path) and isinstance(treshold, int) and treshold >= 0:
            return True
        else:
            print("invalid input: Preprocessed path or treshold is invalid.")
            return False

    # If not using preprocessed data, validate sentences, remove words, and treshold
    if sentences_path is not None and remove_words_path is not None:
        if isinstance(treshold, int) and treshold >= 0:
            if is_valid_csv_path(sentences_path) and is_valid_csv_path(remove_words_path):
                return True
            else:
                print("invalid input: One or more CSV paths are invalid.")
                return False
        else:
            print("invalid input: treshold is invalid.")
            return False
    else:
        print("invalid input: One or more arguments are missing (sentences, remove_words paths, or treshold).")
        return False




def is_valid_csv_path(path):
    # Check if the file exists
    if not os.path.isfile(path):
        return False
    
    # Try opening and reading the file
    try:
        with open(path, mode='r', newline='', encoding='utf-8') as file:
            csv.reader(file)
            return True
    except:
        return False
    


def is_valid_json_path(path):
    # Check if the file exists
    if not os.path.isfile(path):
        return False
    
    # Try opening and reading the file
    try:
        with open(path, mode='r', encoding='utf-8') as file:
            json.load(file)  # Try to parse the JSON
            return True
    except:
        return False



if __name__=="__main__":
    main()
