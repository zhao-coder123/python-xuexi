import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const dogPortrait = staticFile('cosmic-dog.png');
const spaceWarpVideo = staticFile('cosmic-space.mp4');

const scenes = [
  {
    title: '宇宙信号接入',
    subtitle: '电影级太空跃迁 + 神秘生命信号',
    duration: 300,
    accent: '#67e8f9',
    lines: ['Signal source detected', 'Deep space gateway online', 'Unknown lifeform locked'],
  },
  {
    title: '休眠舱苏醒',
    subtitle: '一只毛茸茸的小狗，正在成为本片主角',
    duration: 420,
    accent: '#f9d5a7',
    lines: ['Cryo chamber open', 'Pet Marvel protocol', 'Captain profile loading'],
  },
  {
    title: '小狗舰长档案',
    subtitle: '把静态照片做成全息人物卡',
    duration: 420,
    accent: '#c4b5fd',
    lines: ['Species: fluffy explorer', 'Mood: calm but curious', 'Mission: cross the nebula'],
  },
  {
    title: '穿越星云航道',
    subtitle: '背景持续高速飞行，主角进入宇宙中心镜头',
    duration: 480,
    accent: '#f472b6',
    lines: ['Warp tunnel synchronized', 'Meteor fragments avoided', 'Gravity field stable'],
  },
  {
    title: '终章英雄定格',
    subtitle: '把日常照片，做成一张宇宙大片海报',
    duration: 540,
    accent: '#fbbf24',
    lines: ['Mission complete', 'Cosmic dust settling', 'Captain returns with starlight'],
  },
];

const styles = {
  page: {
    flex: 1,
    backgroundColor: '#020617',
    color: '#f8fafc',
    fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
    overflow: 'hidden',
  },
  overlay: {
    position: 'absolute',
    inset: 0,
    background:
      'linear-gradient(180deg, rgba(2, 6, 23, 0.22) 0%, rgba(2, 6, 23, 0.48) 46%, rgba(2, 6, 23, 0.82) 100%)',
  },
  frame: {
    position: 'relative',
    zIndex: 2,
    height: '100%',
    padding: 56,
    display: 'flex',
    flexDirection: 'column',
  },
  topBar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 24,
    marginBottom: 28,
  },
  tag: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: 10,
    padding: '10px 18px',
    borderRadius: 999,
    backgroundColor: 'rgba(15, 23, 42, 0.6)',
    border: '1px solid rgba(148, 163, 184, 0.2)',
    fontSize: 20,
  },
  title: {
    fontSize: 84,
    lineHeight: 1.04,
    fontWeight: 850,
    letterSpacing: '-0.03em',
    maxWidth: 980,
  },
  subtitle: {
    fontSize: 30,
    lineHeight: 1.45,
    color: '#cbd5e1',
    maxWidth: 880,
    marginTop: 16,
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1.05fr 0.95fr',
    gap: 28,
    flex: 1,
  },
  panel: {
    position: 'relative',
    borderRadius: 32,
    overflow: 'hidden',
    backgroundColor: 'rgba(8, 15, 31, 0.64)',
    border: '1px solid rgba(148, 163, 184, 0.18)',
    backdropFilter: 'blur(12px)',
    boxShadow: '0 24px 80px rgba(2, 6, 23, 0.35)',
  },
  linesWrap: {
    display: 'grid',
    gap: 16,
  },
  lineCard: {
    padding: '18px 22px',
    borderRadius: 22,
    backgroundColor: 'rgba(15, 23, 42, 0.6)',
    border: '1px solid rgba(148, 163, 184, 0.18)',
    fontSize: 28,
    fontWeight: 600,
    color: '#e2e8f0',
  },
  dataGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, minmax(0, 1fr))',
    gap: 18,
    marginTop: 28,
  },
  dataCard: {
    borderRadius: 22,
    padding: 20,
    backgroundColor: 'rgba(8, 15, 31, 0.55)',
    border: '1px solid rgba(148, 163, 184, 0.16)',
  },
  bottomCaption: {
    position: 'absolute',
    left: 56,
    right: 56,
    bottom: 34,
    display: 'flex',
    justifyContent: 'space-between',
    gap: 24,
    fontSize: 20,
    color: '#cbd5e1',
    zIndex: 3,
  },
};

const getSceneStarts = () => {
  let cursor = 0;
  return scenes.map((scene) => {
    const start = cursor;
    cursor += scene.duration;
    return {...scene, start};
  });
};

const timeline = getSceneStarts();

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

const SpaceBackground = ({tint}) => {
  const frame = useCurrentFrame();
  const scale = 1.08 + Math.sin(frame / 38) * 0.02;
  const driftX = Math.sin(frame / 45) * 18;
  const driftY = Math.cos(frame / 52) * 12;

  return (
    <AbsoluteFill>
      <OffthreadVideo
        loop
        muted
        playbackRate={1}
        src={spaceWarpVideo}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${scale}) translate(${driftX}px, ${driftY}px)`,
          filter: 'saturate(1.2) contrast(1.1) brightness(0.75)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `radial-gradient(circle at center, ${tint}22 0%, transparent 40%), radial-gradient(circle at top right, rgba(255,255,255,0.10), transparent 22%)`,
          mixBlendMode: 'screen',
        }}
      />
      <div style={styles.overlay} />
    </AbsoluteFill>
  );
};

const ProgressRail = ({accent, sceneIndex, localFrame, sceneDuration}) => {
  return (
    <div style={{display: 'flex', gap: 10, minWidth: 520}}>
      {timeline.map((scene, index) => {
        const progress = index < sceneIndex ? 1 : index === sceneIndex ? clamp(localFrame / sceneDuration, 0, 1) : 0;

        return (
          <div
            key={scene.title}
            style={{
              flex: 1,
              height: 7,
              borderRadius: 999,
              overflow: 'hidden',
              backgroundColor: 'rgba(148, 163, 184, 0.18)',
            }}
          >
            <div
              style={{
                width: `${progress * 100}%`,
                height: '100%',
                background: `linear-gradient(90deg, ${accent}, rgba(255,255,255,0.95))`,
              }}
            />
          </div>
        );
      })}
    </div>
  );
};

const HoloPortrait = ({accent, mode = 'full'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const entrance = spring({frame, fps, config: {damping: 200, stiffness: 100}});
  const pulse = 1 + Math.sin(frame / 18) * 0.015;
  const spin = frame * 1.4;
  const imageScale = mode === 'close' ? 1.35 : mode === 'poster' ? 1.18 : 1.06;
  const imageX = mode === 'close' ? -34 : 0;
  const imageY = mode === 'poster' ? -28 : -8;

  return (
    <div
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          position: 'absolute',
          width: 620,
          height: 620,
          borderRadius: 999,
          border: `1px solid ${accent}33`,
          transform: `scale(${pulse}) rotate(${spin}deg)`,
          boxShadow: `0 0 48px ${accent}22`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          width: 520,
          height: 520,
          borderRadius: 999,
          border: `2px dashed ${accent}55`,
          transform: `scale(${1.02 - Math.sin(frame / 24) * 0.02}) rotate(${-spin * 0.7}deg)`,
        }}
      />
      <div
        style={{
          position: 'relative',
          width: mode === 'poster' ? 560 : 500,
          height: mode === 'poster' ? 760 : 640,
          borderRadius: mode === 'poster' ? 36 : 999,
          overflow: 'hidden',
          border: `2px solid ${accent}66`,
          backgroundColor: 'rgba(3, 7, 18, 0.84)',
          boxShadow: `0 20px 70px ${accent}30`,
          transform: `scale(${0.9 + entrance * 0.1})`,
        }}
      >
        <Img
          src={dogPortrait}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: mode === 'close' ? '52% 42%' : '50% 42%',
            transform: `scale(${imageScale}) translate(${imageX}px, ${imageY}px)`,
            filter: 'contrast(1.06) saturate(0.95) brightness(1.03)',
          }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: `linear-gradient(180deg, ${accent}18 0%, transparent 28%, transparent 72%, rgba(2,6,23,0.45) 100%)`,
            mixBlendMode: 'screen',
          }}
        />
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: `${(frame * 14) % 110}%`,
            height: 58,
            background: `linear-gradient(180deg, transparent 0%, ${accent} 50%, transparent 100%)`,
            opacity: 0.16,
            filter: 'blur(12px)',
          }}
        />
      </div>
    </div>
  );
};

const SceneShell = ({scene, sceneIndex, children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const entrance = spring({frame, fps, config: {damping: 190, stiffness: 115}});
  const blur = interpolate(frame, [0, 14], [18, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={styles.page}>
      <SpaceBackground tint={scene.accent} />
      <div
        style={{
          ...styles.frame,
          opacity: interpolate(frame, [0, 10, scene.duration - 12, scene.duration], [0, 1, 1, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
          transform: `translateY(${(1 - entrance) * 34}px) scale(${0.96 + entrance * 0.04})`,
          filter: `blur(${blur}px)`,
        }}
      >
        <div style={styles.topBar}>
          <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
            <div style={styles.tag}>Cosmic Dog Odyssey</div>
            <div style={{fontSize: 20, color: '#cbd5e1'}}>Scene {sceneIndex + 1} / {timeline.length}</div>
          </div>
          <ProgressRail accent={scene.accent} localFrame={frame} sceneDuration={scene.duration} sceneIndex={sceneIndex} />
        </div>
        {children}
      </div>
      <div style={styles.bottomCaption}>
        <div>素材结合: `IMG_0983.PNG` + 宇宙穿梭视频</div>
        <div>风格: 科幻海报 / 角色觉醒 / 宇宙航行</div>
      </div>
    </AbsoluteFill>
  );
};

const IntroScene = ({scene, sceneIndex}) => {
  const frame = useCurrentFrame();

  return (
    <SceneShell scene={scene} sceneIndex={sceneIndex}>
      <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', flex: 1}}>
        <div style={{fontSize: 22, color: scene.accent, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase'}}>Deep Space Broadcast</div>
        <div style={styles.title}>{scene.title}</div>
        <div style={styles.subtitle}>{scene.subtitle}</div>
        <div style={{...styles.linesWrap, marginTop: 32, maxWidth: 700}}>
          {scene.lines.map((line, index) => {
            const reveal = interpolate(frame, [20 + index * 10, 36 + index * 10], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });

            return (
              <div
                key={line}
                style={{
                  ...styles.lineCard,
                  opacity: reveal,
                  transform: `translateX(${(1 - reveal) * 40}px)`,
                  borderColor: `${scene.accent}40`,
                }}
              >
                {line}
              </div>
            );
          })}
        </div>
      </div>
    </SceneShell>
  );
};

const RevealScene = ({scene, sceneIndex}) => {
  return (
    <SceneShell scene={scene} sceneIndex={sceneIndex}>
      <div style={styles.grid}>
        <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
          <div style={{fontSize: 20, color: scene.accent, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em'}}>Cryo Chamber</div>
          <div style={styles.title}>{scene.title}</div>
          <div style={styles.subtitle}>{scene.subtitle}</div>
          <div style={{...styles.linesWrap, marginTop: 28}}>
            {scene.lines.map((line) => (
              <div key={line} style={{...styles.lineCard, borderColor: `${scene.accent}40`}}>{line}</div>
            ))}
          </div>
        </div>
        <div style={styles.panel}>
          <HoloPortrait accent={scene.accent} mode="full" />
        </div>
      </div>
    </SceneShell>
  );
};

const DossierScene = ({scene, sceneIndex}) => {
  const frame = useCurrentFrame();
  const cards = [
    ['代号', 'Captain Fluffy'],
    ['特征', 'calm eyes / soft fur / stable aura'],
    ['状态', 'curious but composed'],
    ['任务', '跨越银河并带回星光'],
  ];

  return (
    <SceneShell scene={scene} sceneIndex={sceneIndex}>
      <div style={styles.grid}>
        <div style={styles.panel}>
          <div style={{padding: 28, display: 'flex', flexDirection: 'column', height: '100%'}}>
            <div style={{fontSize: 22, color: scene.accent, fontWeight: 700, marginBottom: 10}}>Character Dossier</div>
            <div style={{fontSize: 64, fontWeight: 850, lineHeight: 1.06}}>小狗舰长档案</div>
            <div style={{fontSize: 28, lineHeight: 1.45, color: '#cbd5e1', marginTop: 18}}>{scene.subtitle}</div>
            <div style={styles.dataGrid}>
              {cards.map(([label, value], index) => {
                const reveal = interpolate(frame, [18 + index * 8, 32 + index * 8], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                });

                return (
                  <div
                    key={label}
                    style={{
                      ...styles.dataCard,
                      opacity: reveal,
                      transform: `translateY(${(1 - reveal) * 18}px)`,
                      borderColor: `${scene.accent}33`,
                    }}
                  >
                    <div style={{fontSize: 18, color: '#94a3b8', marginBottom: 8}}>{label}</div>
                    <div style={{fontSize: 28, fontWeight: 700, lineHeight: 1.35}}>{value}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
        <div style={styles.panel}>
          <HoloPortrait accent={scene.accent} mode="close" />
        </div>
      </div>
    </SceneShell>
  );
};

const WarpScene = ({scene, sceneIndex}) => {
  const frame = useCurrentFrame();

  return (
    <SceneShell scene={scene} sceneIndex={sceneIndex}>
      <div style={{display: 'grid', gridTemplateColumns: '0.92fr 1.08fr', gap: 28, flex: 1}}>
        <div style={styles.panel}>
          <HoloPortrait accent={scene.accent} mode="poster" />
        </div>
        <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
          <div style={{fontSize: 22, color: scene.accent, fontWeight: 700, marginBottom: 12}}>Nebula Run</div>
          <div style={styles.title}>{scene.title}</div>
          <div style={styles.subtitle}>{scene.subtitle}</div>
          <div style={{marginTop: 30, display: 'grid', gap: 18}}>
            {scene.lines.map((line, index) => {
              const scale = 1 + Math.sin((frame + index * 12) / 18) * 0.02;

              return (
                <div
                  key={line}
                  style={{
                    ...styles.lineCard,
                    borderColor: `${scene.accent}55`,
                    transform: `scale(${scale})`,
                  }}
                >
                  {line}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </SceneShell>
  );
};

const FinaleScene = ({scene, sceneIndex}) => {
  return (
    <SceneShell scene={scene} sceneIndex={sceneIndex}>
      <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', flex: 1}}>
        <div style={{width: 760, height: 760, marginBottom: 34}}>
          <HoloPortrait accent={scene.accent} mode="poster" />
        </div>
        <div style={{fontSize: 24, color: scene.accent, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase'}}>Final Poster</div>
        <div style={{fontSize: 92, fontWeight: 900, lineHeight: 1.02, textAlign: 'center', maxWidth: 1240}}>{scene.title}</div>
        <div style={{fontSize: 32, lineHeight: 1.4, color: '#e2e8f0', textAlign: 'center', maxWidth: 980, marginTop: 18}}>{scene.subtitle}</div>
      </div>
    </SceneShell>
  );
};

export const CosmicDogVideo = () => {
  return (
    <AbsoluteFill style={styles.page}>
      {timeline.map((scene, index) => {
        let component = null;

        if (index === 0) component = <IntroScene scene={scene} sceneIndex={index} />;
        if (index === 1) component = <RevealScene scene={scene} sceneIndex={index} />;
        if (index === 2) component = <DossierScene scene={scene} sceneIndex={index} />;
        if (index === 3) component = <WarpScene scene={scene} sceneIndex={index} />;
        if (index === 4) component = <FinaleScene scene={scene} sceneIndex={index} />;

        return (
          <Sequence key={scene.title} from={scene.start} durationInFrames={scene.duration}>
            {component}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
