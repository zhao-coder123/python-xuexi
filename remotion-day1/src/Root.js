import React from 'react';
import {Composition} from 'remotion';
import {Day1Video} from './Day1Video';
import {CosmicDogVideo} from './CosmicDogVideo';
import {totalDurationInFrames} from './day1-data';

export const RemotionRoot = () => {
  return (
    <>
      {/* 一个 Composition 就是一支可单独预览和渲染的视频。 */}
      <Composition
        id="Day1PythonLesson"
        component={Day1Video}
        durationInFrames={totalDurationInFrames}
        fps={30}
        width={1920}
        height={1080}
      />

      <Composition
        id="CosmicDogOdyssey"
        component={CosmicDogVideo}
        durationInFrames={2160}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
