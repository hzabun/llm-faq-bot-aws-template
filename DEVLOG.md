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
