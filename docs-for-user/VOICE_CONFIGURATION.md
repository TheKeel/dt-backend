# 语音配置

TTS/STT 在「设置 → 语音」；图像/视频在「设置 → 多模态生成」。

## Uso

- Volcengine Speech (Doubao)：新控制台填 Speech API Key（App ID 空）；旧控制台填 App ID + Access Token。地址 `https://openspeech.bytedance.com/api/v3`。TTS 选资源 ID（如 `seed-tts-2.0`）+ 同版本音色；STT 模型 `bigmodel`，默认 `volc.bigasr.auc_turbo`。录音转 16kHz WAV 需 ffmpeg。
- 按模型配音色：OpenAI/OpenRouter/火山1.0/2.0/Groq/阿里Qwen HTTP 各用对应列表；CosyVoice 等非 HTTP 协议不支持。列表非全量，可手填 ID（须同协议）。
- 试听：选好音色/语言/参数填文本点试听，不用保存；改配置清旧试听，可取消。一般 ≤500 字符，Groq Orpheus ≤200，会收费。

<details>
<summary>官方文档</summary>

- [火山 TTS](https://www.volcengine.com/docs/6561/1598757) / [音色](https://www.volcengine.com/docs/6561/1257544) / [录音识别](https://www.volcengine.com/docs/6561/1631584)
- [Qwen 音色](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-list)
</details>
