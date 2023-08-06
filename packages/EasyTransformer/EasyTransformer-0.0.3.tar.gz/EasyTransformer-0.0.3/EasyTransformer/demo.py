import EasyTransformer
from EasyTransformer import bert
from EasyTransformer import transformer

lines =[
        "I love NJU",
        "Good morning"
]
Encoder = bert.BERT()
tokenizer=bert.BertTokenizer(lines,30000,512)
list = ["I love NJU", "Good morning"]
indexed_tokens,att_mask,pos,segment_label=tokenizer.encodepro(list[0])
# indexed_tokens = torch.tensor(indexed_tokens)
# pos = torch.tensor(pos)
# segment_label = torch.tensor(segment_label)
out1,out2 = Encoder(indexed_tokens,pos,segment_label)
print(out1.shape)
print(out2.shape)

Encoder = transformer.TransformerEncoder(30000)
tokenizer=transformer.TransformerTokenizer(30000,512,lines)
indexed_tokens=tokenizer.encode(list[1])
out1,out2 = Encoder(indexed_tokens)
print(out1.shape)
print(out2.shape)