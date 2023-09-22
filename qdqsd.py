def main():
    ensure_integrity(persist_directory, False)
    args = parse_arguments()
    embeddings_kwargs = {'device': 'cuda'} if is_gpu_enabled else {}
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, model_kwargs=embeddings_kwargs)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
    match model_type:
        case "LlamaCpp":
            llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, callbacks=callbacks, verbose=False, n_gpu_layers=calculate_layer_count())
        case "GPT4All":
            if is_gpu_enabled:
                print("GPU is enabled, but GPT4All does not support GPU acceleration. Please use LlamaCpp instead.")
                exit(1)
            llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', callbacks=callbacks, verbose=False)
        case _default:
            print(f"Model {model_type} not supported!")
            exit;
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents= not args.hide_source)
