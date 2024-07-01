import streamlit as st


# build dictionary
def load_vocab(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


vocabs = load_vocab(file_path="C:/Users/Admin/Downloads/source/source/data/vocab.txt")


def levenshtein_distance(token1, token2):
    # create a 2D matrix full fill 0s
    distance = [[0] * (len(token2) + 1) for _ in range(len(token1) + 1)]

    for i in range(len(token1) + 1):
        distance[i][0] = i

    for j in range(len(token2) + 1):
        distance[0][j] = j

    a = 0
    b = 0
    c = 0

    for i in range(1, len(token1) + 1):
        for j in range(1, len(token2) + 1):
            # if the characters are the same, no edit is required
            if token1[i - 1] == token2[j - 1]:
                distance[i][j] = distance[i - 1][j - 1]
            else:
                # calculate the costs for insertion, deletion and substitution
                a = distance[i][j - 1]
                b = distance[i - 1][j]
                c = distance[i - 1][j - 1]

                # choose the minimum cost and add 1:
                distance[i][j] = min(a, b, c) + 1

    return distance[len(token1)][len(token2)]


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input("Word: ")
    if st.button("Compute"):
        # compute levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)

        # sorted by distance
        sorted_distances = dict(sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distances.keys())[0]
        st.write("Correct word: ", correct_word)

        col1, col2 = st.columns(2)
        col1.write("Vocabulary: ")
        col1.write(vocabs)

        col2.write("Distance: ")
        col2.write(sorted_distances)


if __name__ == "__main__":
    main()