## 📅 July 12, 2025

#### Done

- [DevOps] Ran containerized app successfully
  - Gemini API key provided as environment variable
- [Docs] Created snippets folder and added to gitignore
  - Folder contains frequently used commands for local development

#### Learned

- Fixed issue with providing gemini API key within the container
  - For local dev: embed environment variable at container startup
  - For AWS deployment: use AWS Parameter Store or Secrets Manager

#### Blockers / Questions

- Nothing today

#### Next steps

- Set up ECS infrastructure via Terraform

## 📅 July 11, 2025

#### Done

- [App] Added dependencies via requirements.txt
- [DevOps] Added initial version of dockerfile

#### Learned

- PDF processing libraries like PyMuPDF require MuPDF to be installed in the OS

#### Blockers / Questions

- Running containerized app not working yet, need to API key within the container

#### Next steps

- Find a secure way to provide API key within the container

## 📅 July 10, 2025

#### Done

- [Docs] Added docstrings to public, more complex functions
- [Docs] Ticket off local MVP phase of the project

#### Learned

- Nothing worth mentioning today

#### Blockers / Questions

- Nothing today

#### Next steps

- Continue with test deployment on AWS

## 📅 July 09, 2025

#### Done

- [App] Converted ChromaDB client to a persistent one
  - When starting the app, it now reuses the existing vectore store

#### Learned

- Nothing worth mentioning today

#### Blockers / Questions

- I wonder how it would make most sense to initialize the chromadb client within a container
  - Persistent client? Remote client?

#### Next steps

- Update readme and get started with next phase

## 📅 July 08, 2025

#### Done

- [App] Connected ChoromaDB to model queries
  - When starting the app, vector store gets initialized and parses the PDF
  - Upon queries, results from the vector store are provided as context string

#### Learned

- FastAPI events `startup` and `shutdown` are deprecated
  - Apparently recommended to use `lifespan` function

#### Blockers / Questions

- Nothing today

#### Next steps

- Create persistent ChromaDB client to store embeddings locally for lower latency

## 📅 July 07, 2025

#### Done

- [App] Added gemini API for basic local MVP testing
  - Gemini offers a free tier perfect for quick dev testing
- [Docs] Added proper MIT license
- [Docs] added environment files to gitignore

#### Learned

- Function `Field` can be used to define validation rules on attributes
  - E.g. minimum length of a prompt parameter must be 1

#### Blockers / Questions

- Nothing today

#### Next steps

- Connect ChromaDB to model queries

## 📅 July 06, 2025

#### Done

- [App] Removed unused library
- [Docs] Added roadmap to readme
  - Split project into four phases
- [Docs] Added placeholder license file
  - Proper license will follow soon

#### Learned

- Nothing worth mentioning today

#### Blockers / Questions

- Nothing today

#### Next steps

- Set up OpenAI API or similar for quick experimenting before containerizing a local LLM

## 📅 July 05, 2025

#### Done

- [App] Added PDF parser
  - Extracts each page of the PDF file
  - Converts pages to text
- [App] Set up ChromaDB as vector store to embed the PDF pages
  - Parsed PDF pages first get semantically chunked based on sentence punctuation via nltk library
  - Then they get embedded into the vector store with their page number as metadata
  - Lastly, a simple query delivers results for the stored chunks

#### Learned

- Remembered the nltk library today and set it up for semantic chunking of text
- Also remembered LlamaIndex, might be worth looking into it again

#### Blockers / Questions

- Nothing today

#### Next steps

- Set up OpenAI API or similar for quick experimenting before containerizing a local LLM

## 📅 July 04, 2025

#### Done

- [App] Added basic FastAPI file
  - Runs in dev mode and prints "hello world"

#### Learned

- FastAPI automatically creates a swagger at the location `/docs/
  - Super handy for development!

#### Blockers / Questions

- Nothing today

#### Next steps

- Read more into how to use FastAPI

## 📅 July 03, 2025

#### Done

- [Infra] Created first basic terraform files
  - Set up provider and remote backend
  - Created placeholder ECS terraform file to be filled later

#### Learned

- Nothing worth mentioning today

#### Blockers / Questions

- Nothing today

#### Next steps

- Continue with basic setup

## 📅 July 02, 2025

#### Done

- [Docs] Created repository for the project
  - Added placeholder project description in readme

#### Learned

- Nothing worth mentioning today

#### Blockers / Questions

- Nothing today

#### Next steps

- Get started with basic setup
