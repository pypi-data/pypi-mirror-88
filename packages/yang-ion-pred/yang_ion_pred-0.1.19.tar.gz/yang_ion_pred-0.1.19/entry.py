import os
import numpy as np
import pandas as pd
import pickle
import joblib
from absl import flags
from absl import app
from emb_vectors import EMB_PATH
from pretrained_model import MODEL_PATH


FLAGS = flags.FLAGS

flags.DEFINE_string(
    name="input",
    default="",
    help="Path to input fasta file"
)

flags.DEFINE_string(
    name="output",
    default="",
    help="Path to output folder"
)


def getAminoAcidEmbedding(embedding_file_path):
    with open(embedding_file_path, "r") as f:
        lines = f.readlines()

    AA_Emb = {}
    for line in lines[1:]:
        temp = line[:-1].split()
        AA_Emb[temp[0]] = temp[1:]
    
    return AA_Emb
        

def convertFastaToFeature(fasta_file_path):
    with open(fasta_file_path, "r") as f:
        lines = f.readlines()

    input_sequences = {}

    fasta_sequence = ""

    temp = lines[0]
    temp = temp.replace(">sp|", "").replace(">", "")

    protein_id = temp[:temp.find("|")]
    for line in lines:
        if line.find(">") < 0:
            if line[-1] == "\n":
                fasta_sequence += line[:-1]
            else:
                fasta_sequence += line
        else:
            input_sequences[protein_id] = fasta_sequence
            temp = line
            temp = temp.replace(">sp|", "").replace(">", "")
            protein_id = temp[:temp.find("|")]
            fasta_sequence = ""

    input_sequences[protein_id] = fasta_sequence
    
    input_segments = {}
    for protein_id in input_sequences.keys():
        sequence = input_sequences.get(protein_id)
        sequence = "OOOOOOO" + sequence + "OOOOOOO"

        segments = []
        for i in range(0, len(sequence)-14):
            segments.append(sequence[i:i+15])

        input_segments[protein_id] = segments
        
    aaEmb = getAminoAcidEmbedding(os.path.join(EMB_PATH, "Emb.vec"))
    
    if not(os.path.exists("tmp")):
        os.mkdir("tmp")

    for protein_id in input_segments.keys():
        with open("tmp/"+protein_id+".csv", "w") as f:
            segments = input_segments.get(protein_id)

            for segment in segments:
                for amino_acid in segment:
#                    f.write(",".join([str(emb_value) for emb_value in aaEmb.get(amino_acid)]))
                    emb_values=aaEmb.get(amino_acid)
                    for emb_value in emb_values:
                        f.write(str(emb_value)+",")
                f.write("\n")
    return input_sequences


def labelToOneHot(label):
    label = label.reshape(len(label), 1)
    label = np.append(label, label, axis=1)
    label[:, 0] = label[:, 0] == 0
    return label


def predict(input_file, output_file="Result.txt"):
    input_sequences = convertFastaToFeature(input_file)
    
    try:
        classifier = joblib.load(os.path.join(MODEL_PATH, "Model.sav"))
    except (IOError, pickle.UnpicklingError, AssertionError):
        print(pickle.UnpicklingError)
        return True
    
    threshold = 0.365

    with open(output_file, "w") as f:
        f.write("No. of sequence = "+str(len(os.listdir("tmp")))+"\n")
        f.write("Predefined threshold: "+str(threshold)+"\n")
        f.write("------------------------------------------------\n")
        f.write("Position     Residue	  Score	     Prediction\n")
        f.write("------------------------------------------------\n")

        for protein_feature_file in os.listdir("tmp"):
            protein_id = protein_feature_file[:-4]
            sequence = input_sequences.get(protein_id)
            length = len(sequence)
            f.write(">"+protein_id+"    Length = "+str(length)+"\n\n")
            f.write(sequence+"\n\n")

            dataset = pd.read_csv("tmp/"+protein_feature_file, header=None)
            X_test = dataset.iloc[:, 0:-1].values
            y_pred = classifier.predict_proba(X_test)
            for i in range(len(y_pred)-2):
                if sequence[i] == "N":
                    if y_pred[i][1] >= threshold:
                        f.write("{:5.0f}".format(i+1)
                                + "    "
                                + sequence[i:i+3]
                                + "    "
                                + "{:10.4f}".format(y_pred[i][1])
                                + "    Potential glycosylated\n")
                    else:
                        f.write("{:5.0f}".format(i+1)
                                + "    "
                                + sequence[i:i+3]
                                + "    "
                                + "{:10.4f}".format(y_pred[i][1])
                                + "    Non-glycosylated\n")

            f.write("***********************************\n\n")


def start(argv):
    input_file_path = FLAGS.input
    output_path = FLAGS.output

    predict(input_file_path, output_file=os.path.join(output_path, "Result.txt"))

    for filename in os.listdir("tmp"):
        os.remove(os.path.join("tmp", filename))

#    print("Thank you for using NIonPred!!! Please check the prediction results in Result.txt file")
    with open("Result.txt", "r") as f:
        print(f.read())

def run():
    app.run(start)    

if __name__ == "__main__":
    run()
