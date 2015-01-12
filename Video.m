mov=VideoReader('##Address of Video##');
nFrames=mov.NumberOfFrames;
for i=1:6:nFrames
  videoFrame=read(mov,i);
  imwrite(videoFrame,['##Address of where to save##' num2str(i) '.jpg'])
end
