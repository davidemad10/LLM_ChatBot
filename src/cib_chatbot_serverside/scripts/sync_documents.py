"""Document synchronization script - watches for new files and processes them."""
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain_community.document_loaders import UnstructuredMarkdownLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from ..config.settings import settings
from ..db.operations import save_to_pgvector


class NewFileHandler(FileSystemEventHandler):
    """Handler for new file events."""
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            file_ext = os.path.splitext(event.src_path)[1].lower()
            if file_ext in [".md", ".pdf"]:
                print(f"New file detected: {event.src_path}")
                self.wait_and_process(event.src_path)

    def wait_and_process(self, file_path, retries=5, delay=1):
        """Wait for the file to be released by the OS before processing."""
        for i in range(retries):
            try:
                with open(file_path, 'rb'):
                    break
            except IOError:
                print(f"File locked, retrying in {delay}s... ({i+1}/{retries})")
                time.sleep(delay)
        else:
            print(f"Could not access file {file_path} after {retries} retries.")
            return

        process_file(file_path)


def process_file(file_path: str):
    """Process a single file - load, chunk, and save to database."""
    print(f"Processing file: {file_path}")
    
    # 1. Load specific file
    if file_path.endswith(".md"):
        loader = UnstructuredMarkdownLoader(file_path)
    else:
        loader = PyPDFLoader(file_path)
    
    documents = loader.load()

    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Add unique IDs to chunks to prevent duplicates
    chunks_with_ids = calculate_chunk_ids(chunks)

    # 4. Save only new chunks
    save_to_pgvector(chunks_with_ids)
    print(f"File processed successfully: {file_path}")


def calculate_chunk_ids(chunks: list[Document]) -> list[Document]:
    """Calculate unique IDs for document chunks."""
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page", 0)
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id

    return chunks


def main():
    """Main function to sync documents."""
    data_path = settings.DATA_PATH
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        print(f"Created data directory: {data_path}")

    # Initial sync for existing files
    print("Performing initial sync...")
    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        if os.path.isfile(file_path) and file_path.endswith(('.md', '.pdf')):
            try:
                process_file(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    # Start watching for new files
    print(f"\nWatching for new files in: {data_path}")
    print("Press Ctrl+C to stop...")
    
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, data_path, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping file watcher...")
    observer.join()


if __name__ == "__main__":
    main()
