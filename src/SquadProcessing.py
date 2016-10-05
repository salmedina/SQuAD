from __future__ import division
import sys
import json
from textblob import TextBlob

def sweep_through_data(target_data):
    # The structure of the train/test QA files is the following:
    #  - title
    #  - paragraphs
    #      - context
    #      - qas
    #          - question
    #          - id
    #          - answers
    #              - text
    #              - answer_start
    #
    # The index described in *answer_start* is 0 based.


    # ## Dataset exploration boilerplate code
    # Traverse all the qa's and store them into a file
    total_topics = 0
    total_questions = 0
    qa_json_path = 'all_questions.json'
    qa_json = []
    for topic in target_data:
        total_topics += 1
        for passage in topic['paragraphs']:
            #print passage['context']
            for qa in passage['qas']:
                total_questions += 1
                #print 'Q%d %s'%(qidx,qa['question'])
                #print 'QID:',qa['id']
                num_ans = 0
                for answer in qa['answers']:
                    #print 'A%d %s'%(aidx,answer['text'])
                    #print 'StartIdx:',answer['answer_start']
                    cur_qa ={}
                    cur_qa['question']=qa['question']
                    cur_qa['answer'] = answer['text']
                    qa_json.append(cur_qa)
                    num_ans += 1

    json.dump(qa_json, open(qa_json_path,'wb'))

    print 'Total topics:    %d'%(total_topics)
    print 'Total questions: %d'%(total_questions)
    print 'Total qa\'s:     %d'%(len(qa_json))
    print 'qa sample:'
    print qa_json[0]


def in_which_sentence(text_blob, char_pos):
    '''
    @:param text_blob: the text blob of the passage
    @:param char_pos: the starting position of the answer (assume answer is only within one sentence)
    Returns: index of the sentence that contains the answer
    The index returned is 0 based
    '''
    if char_pos < 0 or char_pos > len(text_blob):
        return -1
    sent_lim = [ s.end for s in text_blob.sentences]
    for pos, lim in zip(range(len(sent_lim)),sent_lim):
        if char_pos < lim:
            return pos
    return -1


def process_data(target_data, save_path):
    # Meta-data Registers
    # 10k indicates the topic id
    # units indicate the passage id within the unit
    topic_id = 10000
    topic_id_inc = 10000
    start_passage_id = 1
    progressive_id_inc = 1
    passage_id = topic_id + start_passage_id

    # Processed QA JSON Structure
    # proc_qa is a list of topics:
    # 	- topic : str
    # 	- paragraphs : []
    # 		- pid : int
    # 		- sentences: []
    # 			- text : str
    # 			- pos : int
    # 			- start_idx : int
    # 		- qas: []
    # 			- qid : int
    # 			- question : str
    # 			- answers:
    # 				- sent_pos : int
    # 				- text : str
    # 				- answer_start : int

    processed_qa = []
    # Process the info
    for topic in target_data:
        print topic['title'] #To keep track of the progress
        qa_topic = {}
        qa_topic['topic'] = topic['title']

        # For each PARAGRAPH
        passage_list = []
        for paragraph in topic['paragraphs']:
            passage = TextBlob(paragraph['context']) #This helps extract the sentences
            # ADD sentences to list to be indexed
            new_passage = {}
            new_passage['pid'] = passage_id
            sentence_list = []
            for pos, sent, raw_sent in zip(range(len(passage.sentences)), passage.sentences, passage.raw_sentences):
                new_sent_input = {}
                new_sent_input['text'] = raw_sent
                new_sent_input['pos'] = pos
                new_sent_input['start_idx'] = sent.start
                sentence_list.append(new_sent_input)

            new_passage['sentences'] = sentence_list

            # Then store the corresponding QA's in another structure for JSON file
            qas_list = []
            for qa in paragraph['qas']:
                new_qa_input = {}
                new_qa_input['qid'] = qa['id']
                new_qa_input['question'] = qa['question']
                answer_list = []
                for answer in qa['answers']:
                    answer['sent_pos'] = in_which_sentence(passage, answer['answer_start'])
                    if answer['sent_pos']==-1:
                        print qa['id']
                    answer_list.append(answer)
                new_qa_input['answers'] = answer_list
                qas_list.append(new_qa_input)

            new_passage['qas'] = qas_list

            passage_list.append(new_passage)

            # Update intra-topic passage id
            passage_id += progressive_id_inc

        qa_topic['paragraphs'] = passage_list

        processed_qa.append(qa_topic)

        # Update the passage id for next topic
        topic_id += topic_id_inc
        passage_id = topic_id + start_passage_id


    json.dump(processed_qa, open(save_path, 'wb'))

if __name__=='__main__':
    if len(sys.argv) < 3:
        print '''Usage: SquadProcessing.py <squad_file> <save_file>'''
        sys.exit(-1)

    squad_filepath = sys.argv[1]
    save_path = sys.argv[2]

    target_json = json.load(open(squad_filepath, 'r'))
    target_data = target_json['data']


    process_data(target_data, save_path)