# acp-extraction

### NGAC.py
Extracts Association, Prohibition and Assignment relations in NGAC format from a given text document. <br /> <br /> To run - `python NGAC.py <DOCUMENT.docx>`
<br /> <br /> 
The text is run through AllenNLP's conference resolution model (demo found here - https://demo.allennlp.org/coreference-resolution).<br /> 
Each sentence is then run through the SRL model (demo found here - https://demo.allennlp.org/semantic-role-labeling). The sentences with labels "B-ARG0" and "B-ARG1" are used to create Association relations. Additionally, Sentences with "B-ARGM-NEG" Labels are used to determine if it is a Prohibition Relations. Sentneces with verbs such as ['contains' , 'includes' , 'include', 'contain', 'is'] are used to create assignment relations. 
