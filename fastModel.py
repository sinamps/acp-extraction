import fasttext
model = fasttext.train_supervised(input="ACP.preprocessed.txt", epoch=25, lr =1.0)
model.save_model("Model_ACP.bin")
print(model.test("ACP.valid"))
