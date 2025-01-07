import fitz  # PyMuPDF 用于 PDF 文本提取
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core import VectorStoreIndex
from llama_index.core import Document
from llama_index.core.indices.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.postprocessor import SentenceTransformerRerank
from typing import Optional


# 从PDF文件中提取文本的函数
def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        # 使用 PyMuPDF 打开 PDF 文件
        document = fitz.open(pdf_path)
        text = ""

        # 提取每一页的文本内容
        for page_num in range(document.page_count):
            page = document.load_page(page_num)  # 加载页面
            text += page.get_text()  # 提取文本
            print(page_num)

        text = text.replace("\n", " ").replace("\r", "")
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


# RAGEngine 类
class RAGEngine:
    def __init__(self, api_key, base_url, pdf_path: str, window_size=3):
        # 初始化 OpenAI 模型和嵌入模型
        self.llm = OpenAI(
            model="gpt-3.5-turbo",
            api_key=api_key,
            api_base=base_url,
            temperature=0.1
        )

        self.embed_model = OpenAIEmbedding(
            model_name="text-embedding-3-small",
            api_key=api_key,
            api_base=base_url
        )

        # 初始化 SentenceWindowNodeParser
        self.node_parser = SentenceWindowNodeParser.from_defaults(
            window_size=window_size,
            window_metadata_key="window",
            original_text_metadata_key="original_text"
        )

        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.node_parser = self.node_parser

        # 从 PDF 文件提取文本
        document_text = extract_text_from_pdf(pdf_path)

        if document_text:
            # 使用 Document 对象
            document = Document(text=document_text)
        else:
            raise ValueError(f"PDF file {pdf_path} could not be processed.")

        # 直接使用 Document 对象创建 VectorStoreIndex
        self.sentence_index = VectorStoreIndex.from_documents(
            [document], service_context=Settings
        )
        print("KKKKKK")
        # 后处理和重排名
        self.postproc = MetadataReplacementPostProcessor(target_metadata_key="window")
        self.rerank = SentenceTransformerRerank(
            top_n=2, model="model"
        )

        # 设置查询引擎
        self.query_engine = self.sentence_index.as_query_engine(
            similarity_top_k=6, node_postprocessors=[self.postproc, self.rerank]
        )

    def query(self, input_text: str, top_k: Optional[int] = 3):
        try:
            # 构造查询请求
            request = {
                "question": input_text,
                "top_k": top_k
            }
            print("OKOK")
            # 获取查询结果
            response = self.query_engine.query(request["question"])
            results = self.sentence_index.as_retriever(
                similarity_top_k=request["top_k"]
            ).retrieve(request["question"])

            # 格式化结果
            formatted_results = []
            for r in results:
                item = {
                    "text": r.node.text.strip(),  # 去除额外空格
                    "score": round(r.score, 4)  # 将分数四舍五入到4位
                }
                formatted_results.append(item)

            # 返回查询结果
            return {
                "answer": str(response),
                "top_k_list": formatted_results
            }

        except Exception as e:
            # 提供更多错误细节，帮助调试
            return {"error": f"An error occurred: {str(e)}. Input text: '{input_text}'"}


# 示例：从 PDF 文件路径中传入文档内容
def query_from_pdf(input_text: str, top_k: Optional[int] = 3):
    print("OK")
    rag_engine = RAGEngine(
        api_key="sk-V4EIJ5P2IyM8EJ8CAsSgIPvubtMa2h7SlaegX0CzqeSzq1Bl",
        base_url="https://api.chatanywhere.org/v1",
        pdf_path="papers_summary.pdf"  # PDF 文件路径
    )
    return rag_engine.query(input_text, top_k)

# # 使用示例
# result = query_from_pdf("What is the summary of the paper?", top_k=6)
# print(result)
