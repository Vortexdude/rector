# rector
Manupulate the image as per the given tensor model

### Common FFmpeg Encodes for Audio

#### MP3 (MPEG-1 Audio Layer III)

```commandline
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3
```
`-codec:a libmp3lame` Specifies the MP3 encoder. </br>
`-qscale:a 2` Sets the quality level (0 is highest, 9 is lowest).

#### AAC (Advanced Audio Codec)


```commandline
ffmpeg -i input.wav -codec:a aac -b:a 192k output.m4a
```
`-codec:a aac` Specifies the AAC encoder.
`-b:a 192k` Sets the audio bitrate to 192 kbps.


#### FLAC (Free Lossless Audio Codec)


```commandline
ffmpeg -i input.wav -codec:a flac output.flac
```
`-codec:a flac` Specifies the FLAC encoder.

#### Opus

```commandline
ffmpeg -i input.wav -codec:a libopus -b:a 128k output.opus
```
`-codec:a libopus` Specifies the Opus encoder.
`-b:a 128k` Sets the audio bitrate to 128 kbps.

### Common FFmpeg Encodes for Video

#### H.264 (MPEG-4 Part 10)

```commandline
ffmpeg -i input.mov -codec:v libx264 -preset medium -crf 23 -codec:a aac -b:a 192k output.mp4
```
`-codec:v libx264` Specifies the H.264 video encoder. </br>
`-preset medium` Sets the encoding speed/quality trade-off. </br>
`-crf 23` Sets the Constant Rate Factor (quality, lower is better). </br>
`-codec:a aac -b:a 192k` Specifies the AAC audio encoder and bitrate. </br>
`H.265` (HEVC - High Efficiency Video Coding)

```commandline
ffmpeg -i input.mov -codec:v libx265 -preset medium -crf 28 -codec:a aac -b:a 192k output.mp4
```

`-codec:v libx265` Specifies the H.265 video encoder.
`-preset medium` Sets the encoding speed/quality trade-off.
`-crf 28` Sets the Constant Rate Factor (quality, lower is better).
`-codec:a aac -b:a 192k` Specifies the AAC audio encoder and bitrate.

#### VP9

```commandline
ffmpeg -i input.mov -codec:v libvpx-vp9 -b:v 2M -codec:a libopus -b:a 128k output.webm
```

`-codec:v libvpx-vp9` Specifies the VP9 video encoder.
`-b:v 2M` Sets the video bitrate to 2 Mbps.
`-codec:a libopus -b:a 128k` Specifies the Opus audio encoder and bitrate.

#### AV1

```commandline
ffmpeg -i input.mov -codec:v libaom-av1 -crf 30 -b:v 0 -codec:a libopus -b:a 128k output.mkv
```
`-codec:v libaom-av1` Specifies the AV1 video encoder. </br>
`-crf 30 -b:v 0` Sets the Constant Rate Factor (quality) and bitrate control. </br>
`-codec:a libopus -b:a 128k` Specifies the Opus audio encoder and bitrate. </br>

Example Commands for Combining Audio and Video Transformation

#### Convert and Compress Video

```commandline
ffmpeg -i input.mov -codec:v libx264 -preset fast -crf 22 -codec:a aac -b:a 128k output.mp4
```
Converts the input video to `H.264` with a specific quality and compresses the audio to AAC.

#### Extract Audio from Video
```commandline
ffmpeg -i input.mp4 -q:a 0 -map a output.mp3
```
Extracts audio from a video file and saves it as an MP3.

`-q:a 0` Sets the audio quality to the highest. </br>

Convert Video to a Different Format

```commandline
ffmpeg -i input.mov -codec:v libvpx -b:v 1M -codec:a libvorbis -b:a 128k output.webm
```
Converts the input video to VP8 format with Vorbis audio.