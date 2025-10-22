# Ren'Py + LMStudio Conversation Demo

A minimal Ren'Py "stub" project that shows how to call a locally-running LLM (via LM Studio) to have a conversation with. Use this as a base for your own Ren'Py + LLM experiments!

## Prerequisites

1. **Ren'Py**  (download at https://www.renpy.org/ - Version used to create this was 8.2.2	)
2. **LM Studio** (download & install from [https://lmstudio.ai](https://lmstudio.ai))  
3. A downloaded model in LM Studio (e.g. gemma-3-4b)
   - Open LM Studio’s **Discover** tab, find your model (e.g. Gemma 3 4B), click **Download**
   - In the **Developer** tab, select the model and click **Start Server**  
   - Note the generated URL (default: `http://127.0.0.1:1234/v1/completions`)

## How to run

1. Download source, e.g. with `git clone https://github.com/YenR/llm-demo-renpy.git`
2. Start LLM Server (see above)
3. Start Ren'Py 
4. Select the folder with the cloned repository as Ren'Py source folder (Preferences -> General -> Projects Directory) 
5. Optionally, open the file `script.rpy` and adjust `MODEL_NAME` and `LMSTUDIO_BASE` 
7. Run the Ren'Py project through the Ren'Py launcher