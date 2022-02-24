# acp-extraction

### NGAC.py
Extracts Association, Prohibition and Assignment relations in NGAC format from a given text document. 
<br /> <br /> 
The text is run through AllenNLP's conference resolution model (demo found here - https://demo.allennlp.org/coreference-resolution).<br /> 
Each sentence is then run through the SRL model (demo found here - https://demo.allennlp.org/semantic-role-labeling). The sentences with labels "B-ARG0" and "B-ARG1" are used to create Association relations. Additionally, Sentences with "B-ARGM-NEG" Labels are used to determine if it is a Prohibition Relations. Sentneces with verbs such as ['contains' , 'includes' , 'include', 'contain', 'is'] are used to create assignment relations. <br /> <br /> To run - `python NGAC.py <DOCUMENT.docx>` <br / ><br /> 
### Requirements
`pip install allennlp==2.1.0 allennlp-models==2.1.0`


### fastModel.py
Implements the fasttext model. Demo can be found here - https://fasttext.cc/docs/en/supervised-tutorial.html. <br />
The data used in the model is a compilation of 4 ACP labeled datasents found here - https://sites.google.com/site/accesscontrolruleextraction/labelled-data-sets <br /> 
The dataset is preprocessed to include format as processed by fasttext. ACP.valid contains 70% of the dataset used for training and ACP.valid contains 30%. <br />
Results -> Precision - 98% ; Recall - 98% <br /> <br /> To run - `python fastModel.py` <br /><br />
### Requirements
`wget https://github.com/facebookresearch/fastText/archive/v0.9.2.zip`<br />
`unzip v0.9.2.zip`<br />
`cd fastText-0.9.2`<br />
#### for command line tool :
`make`<br />
#### for python bindings :
`pip install .`<br />
