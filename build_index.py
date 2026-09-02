from rag_core import RAGIndex, EMBED_DIM

if __name__ == "__main__":
    print(">>> RAG 인덱스 생성 시작")

    idx = RAGIndex(dim=EMBED_DIM)

    idx.build_from_folder("data/law_corpus")

    idx.save(
        "indexes/law_faiss.index",
        "indexes/law_texts.txt",
        "indexes/law_embs.npy",
    )

    print(">>> 인덱스 생성 완료")
