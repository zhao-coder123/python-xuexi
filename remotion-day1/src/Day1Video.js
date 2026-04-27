import React from 'react';
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {
  checklistItems,
  checklistScene,
  day1Overview,
  introScene,
  runScene,
  sections,
  summaryScene,
} from './day1-data';

const bg = '#04101b';
const panel = 'rgba(8, 18, 34, 0.82)';
const panelAlt = 'rgba(15, 23, 42, 0.72)';
const panelBorder = 'rgba(148, 163, 184, 0.18)';
const textMain = '#e2e8f0';
const textMuted = '#94a3b8';
const monoFont = 'SFMono-Regular, Menlo, Consolas, monospace';

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

const chapterDefinitions = [
  {
    key: 'intro',
    kind: 'intro',
    label: introScene.title,
    accent: introScene.accent,
    durationInFrames: introScene.durationInFrames,
    narration: introScene.narration,
  },
  {
    key: 'checklist',
    kind: 'checklist',
    label: checklistScene.title,
    accent: checklistScene.accent,
    durationInFrames: checklistScene.durationInFrames,
    narration: checklistScene.narration,
  },
  ...sections.map((section, index) => ({
    key: `section-${index}`,
    kind: 'section',
    label: section.title,
    accent: section.accent,
    durationInFrames: section.durationInFrames,
    narration: section.narration,
    section,
    sectionIndex: index,
  })),
  {
    key: 'run',
    kind: 'run',
    label: runScene.title,
    accent: runScene.accent,
    durationInFrames: runScene.durationInFrames,
    narration: runScene.narration,
  },
  {
    key: 'summary',
    kind: 'summary',
    label: summaryScene.title,
    accent: summaryScene.accent,
    durationInFrames: summaryScene.durationInFrames,
    narration: summaryScene.narration,
  },
];

const chapterTimeline = (() => {
  let cursor = 0;

  return chapterDefinitions.map((chapter, index) => {
    const start = cursor;
    const enriched = {
      ...chapter,
      sceneIndex: index,
      start,
      end: start + chapter.durationInFrames,
    };

    cursor += chapter.durationInFrames;
    return enriched;
  });
})();

const subtitleTrack = (() => {
  const items = [];

  chapterTimeline.forEach((chapter) => {
    let localCursor = 0;

    chapter.narration.forEach((cue, cueIndex) => {
      items.push({
        ...cue,
        cueIndex,
        chapterLabel: chapter.label,
        accent: chapter.accent,
        start: chapter.start + localCursor,
        end: chapter.start + localCursor + cue.frames,
      });

      localCursor += cue.frames;
    });
  });

  return items;
})();

const styles = {
  page: {
    flex: 1,
    backgroundColor: bg,
    color: textMain,
    fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
    padding: 56,
    overflow: 'hidden',
  },
  content: {
    position: 'relative',
    zIndex: 2,
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 28,
    marginBottom: 26,
  },
  headerLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: 18,
  },
  tag: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: 10,
    padding: '10px 18px',
    borderRadius: 999,
    backgroundColor: 'rgba(15, 23, 42, 0.76)',
    border: `1px solid ${panelBorder}`,
    fontSize: 20,
    color: textMuted,
  },
  dot: (color) => ({
    width: 10,
    height: 10,
    borderRadius: 999,
    backgroundColor: color,
  }),
  headerTitle: {
    fontSize: 22,
    color: textMuted,
  },
  progressWrap: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    minWidth: 560,
  },
  progressSegment: {
    position: 'relative',
    height: 8,
    flex: 1,
    borderRadius: 999,
    backgroundColor: 'rgba(148, 163, 184, 0.16)',
    overflow: 'hidden',
  },
  sectionGrid: {
    display: 'grid',
    gridTemplateColumns: '1.1fr 0.9fr',
    gap: 28,
    flex: 1,
  },
  panel: {
    position: 'relative',
    backgroundColor: panel,
    border: `1px solid ${panelBorder}`,
    borderRadius: 32,
    padding: 30,
    boxShadow: '0 24px 90px rgba(2, 8, 23, 0.35)',
    backdropFilter: 'blur(10px)',
  },
  panelAlt: {
    backgroundColor: panelAlt,
  },
  eyebrow: {
    fontSize: 19,
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
    fontWeight: 700,
    marginBottom: 14,
  },
  heroTitle: {
    fontSize: 92,
    lineHeight: 1.02,
    fontWeight: 850,
    margin: '10px 0 18px',
    maxWidth: 1120,
  },
  heroSubtitle: {
    fontSize: 42,
    fontWeight: 700,
    marginBottom: 20,
  },
  heroText: {
    fontSize: 33,
    lineHeight: 1.5,
    color: textMuted,
    maxWidth: 980,
  },
  sectionTitle: {
    fontSize: 60,
    lineHeight: 1.06,
    fontWeight: 800,
    marginBottom: 16,
  },
  conceptText: {
    fontSize: 28,
    lineHeight: 1.45,
    color: '#dbeafe',
    marginBottom: 22,
  },
  bulletItem: {
    display: 'flex',
    gap: 16,
    alignItems: 'flex-start',
    marginBottom: 18,
  },
  bulletText: {
    fontSize: 30,
    lineHeight: 1.45,
  },
  chipRow: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: 12,
    marginTop: 22,
  },
  chip: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '10px 16px',
    borderRadius: 999,
    backgroundColor: 'rgba(15, 23, 42, 0.88)',
    border: `1px solid ${panelBorder}`,
    fontSize: 21,
    color: '#dbeafe',
  },
  codeWindow: {
    position: 'relative',
    overflow: 'hidden',
    borderRadius: 30,
    backgroundColor: '#020617',
    border: '1px solid rgba(148, 163, 184, 0.16)',
    minHeight: 520,
  },
  codeHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '18px 22px',
    borderBottom: '1px solid rgba(148, 163, 184, 0.12)',
    color: textMuted,
    fontSize: 19,
  },
  codeBody: {
    padding: '18px 20px 26px',
  },
  codeLine: {
    display: 'grid',
    gridTemplateColumns: '56px 1fr',
    gap: 12,
    alignItems: 'start',
    borderRadius: 16,
    padding: '4px 10px',
    marginBottom: 6,
    fontSize: 25,
    lineHeight: 1.7,
    fontFamily: monoFont,
    whiteSpace: 'pre-wrap',
  },
  lineNumber: {
    color: '#64748b',
    textAlign: 'right',
  },
  statCard: {
    position: 'relative',
    padding: '18px 20px',
    borderRadius: 24,
    backgroundColor: 'rgba(8, 18, 34, 0.72)',
    border: `1px solid ${panelBorder}`,
    fontSize: 28,
    fontWeight: 700,
    boxShadow: '0 22px 50px rgba(2, 8, 23, 0.24)',
  },
  orbitStage: {
    position: 'relative',
    width: 440,
    height: 440,
    margin: '0 auto',
  },
  centerOrb: {
    position: 'absolute',
    left: '50%',
    top: '50%',
    width: 200,
    height: 200,
    marginLeft: -100,
    marginTop: -100,
    borderRadius: 999,
    background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.26), rgba(15, 23, 42, 0.94))',
    border: `1px solid ${panelBorder}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    textAlign: 'center',
    fontSize: 28,
    fontWeight: 800,
    padding: 20,
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    gap: 20,
    marginTop: 20,
    fontSize: 21,
    color: textMuted,
  },
  subtitleShell: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 26,
    display: 'flex',
    justifyContent: 'center',
    zIndex: 20,
    pointerEvents: 'none',
  },
  subtitleBox: {
    width: 1220,
    borderRadius: 28,
    padding: '18px 22px 20px',
    backgroundColor: 'rgba(2, 6, 23, 0.78)',
    border: '1px solid rgba(148, 163, 184, 0.18)',
    backdropFilter: 'blur(14px)',
    boxShadow: '0 18px 60px rgba(2, 6, 23, 0.45)',
  },
  subtitleText: {
    fontSize: 34,
    lineHeight: 1.45,
    fontWeight: 700,
    color: '#f8fafc',
    textAlign: 'center',
  },
  callout: {
    borderRadius: 26,
    padding: 24,
    backgroundColor: 'rgba(15, 23, 42, 0.86)',
    border: `1px solid ${panelBorder}`,
  },
};

const AnimatedBackdrop = ({accent}) => {
  const frame = useCurrentFrame();
  const drift = Math.sin(frame / 28) * 40;
  const driftAlt = Math.cos(frame / 35) * 26;

  return (
    <>
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, #020817 0%, #04101b 42%, #07131f 100%)',
        }}
      />
      <AbsoluteFill
        style={{
          opacity: 0.38,
          backgroundImage:
            'linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px)',
          backgroundSize: '90px 90px',
          transform: `translate(${drift * 0.3}px, ${driftAlt * 0.3}px)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -100,
          top: 120 + drift * 0.3,
          width: 420,
          height: 420,
          borderRadius: 999,
          filter: 'blur(32px)',
          background: `radial-gradient(circle, ${accent}44 0%, transparent 70%)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          right: 70,
          top: 80 + driftAlt,
          width: 320,
          height: 320,
          borderRadius: 999,
          filter: 'blur(18px)',
          background: 'radial-gradient(circle, rgba(251, 191, 36, 0.20) 0%, transparent 72%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background:
            'radial-gradient(circle at top right, rgba(56, 189, 248, 0.12), transparent 25%), radial-gradient(circle at bottom left, rgba(168, 85, 247, 0.10), transparent 28%)',
        }}
      />
    </>
  );
};

const ProgressHeader = ({sceneIndex, title, accent, durationInFrames}) => {
  const frame = useCurrentFrame();

  return (
    <div style={styles.header}>
      <div style={styles.headerLeft}>
        <div style={{...styles.tag, color: '#e2e8f0'}}>
          <div style={styles.dot(accent)} />
          Day 1 Teaching Video
        </div>
        <div style={styles.headerTitle}>{title}</div>
      </div>
      <div style={styles.progressWrap}>
        {chapterTimeline.map((chapter, index) => {
          const fill = index < sceneIndex ? 1 : index === sceneIndex ? clamp(frame / durationInFrames, 0, 1) : 0;

          return (
            <div key={chapter.key} style={styles.progressSegment}>
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  transformOrigin: 'left center',
                  transform: `scaleX(${fill})`,
                  background: `linear-gradient(90deg, ${chapter.accent}, rgba(255, 255, 255, 0.95))`,
                }}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};

const PageShell = ({children, accent, sceneIndex, title, durationInFrames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const entrance = spring({
    frame,
    fps,
    config: {damping: 200, stiffness: 110},
  });
  const opacity = interpolate(frame, [0, 10, durationInFrames - 10, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const exitLift = interpolate(frame, [durationInFrames - 16, durationInFrames], [0, -20], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{...styles.page, opacity}}>
      <AnimatedBackdrop accent={accent} />
      <div
        style={{
          ...styles.content,
          transform: `translateY(${(1 - entrance) * 34 + exitLift}px) scale(${0.97 + entrance * 0.03})`,
        }}
      >
        <ProgressHeader
          accent={accent}
          durationInFrames={durationInFrames}
          sceneIndex={sceneIndex}
          title={title}
        />
        {children}
      </div>
    </AbsoluteFill>
  );
};

const BulletList = ({items, accent}) => {
  const frame = useCurrentFrame();

  return (
    <div>
      {items.map((item, index) => {
        const reveal = interpolate(frame, [10 + index * 7, 20 + index * 7], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

        return (
          <div
            key={item}
            style={{
              ...styles.bulletItem,
              opacity: reveal,
              transform: `translateX(${(1 - reveal) * 24}px)`,
            }}
          >
            <div
              style={{
                width: 14,
                height: 14,
                marginTop: 16,
                borderRadius: 999,
                backgroundColor: accent,
                boxShadow: `0 0 18px ${accent}`,
                flexShrink: 0,
              }}
            />
            <div style={styles.bulletText}>{item}</div>
          </div>
        );
      })}
    </div>
  );
};

const ChipRow = ({chips, accent}) => {
  const frame = useCurrentFrame();

  return (
    <div style={styles.chipRow}>
      {chips.map((chip, index) => {
        const reveal = interpolate(frame, [22 + index * 4, 30 + index * 4], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

        return (
          <div
            key={chip}
            style={{
              ...styles.chip,
              opacity: reveal,
              transform: `translateY(${(1 - reveal) * 18}px)`,
              borderColor: `${accent}55`,
              color: accent,
            }}
          >
            {chip}
          </div>
        );
      })}
    </div>
  );
};

const StatCards = ({items, accent}) => {
  const frame = useCurrentFrame();

  return (
    <div style={{display: 'grid', gap: 16}}>
      {items.map((item, index) => {
        const floatY = Math.sin((frame + index * 10) / 24) * 8;
        const reveal = interpolate(frame, [8 + index * 10, 18 + index * 10], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

        return (
          <div
            key={item}
            style={{
              ...styles.statCard,
              opacity: reveal,
              transform: `translateY(${floatY + (1 - reveal) * 22}px)`,
              borderColor: `${accent}44`,
            }}
          >
            {item}
          </div>
        );
      })}
    </div>
  );
};

const OrbitCluster = ({items, accent, centerLabel}) => {
  const frame = useCurrentFrame();

  return (
    <div style={styles.orbitStage}>
      <div style={{...styles.centerOrb, boxShadow: `0 0 60px ${accent}25`}}>{centerLabel}</div>
      {items.map((item, index) => {
        const angle = (index / items.length) * Math.PI * 2 + frame / 45;
        const radius = 164 + Math.sin(frame / 18 + index) * 10;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        return (
          <div
            key={item}
            style={{
              position: 'absolute',
              left: '50%',
              top: '50%',
              transform: `translate(${x - 70}px, ${y - 24}px)`,
              width: 140,
              padding: '10px 14px',
              borderRadius: 999,
              textAlign: 'center',
              fontSize: 22,
              fontWeight: 700,
              color: '#e2e8f0',
              backgroundColor: 'rgba(8, 18, 34, 0.88)',
              border: `1px solid ${accent}55`,
              boxShadow: `0 0 22px ${accent}22`,
            }}
          >
            {item}
          </div>
        );
      })}
    </div>
  );
};

const CodePanel = ({title, lines, accent, terminal = false}) => {
  const frame = useCurrentFrame();
  const activeLine = Math.min(lines.length - 1, Math.floor(frame / 18));
  const scanline = (frame * 18) % 460;

  return (
    <div style={styles.codeWindow}>
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: scanline,
          height: 90,
          opacity: 0.12,
          background: `linear-gradient(180deg, transparent 0%, ${accent} 50%, transparent 100%)`,
          filter: 'blur(18px)',
        }}
      />
      <div style={styles.codeHeader}>
        <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
          <div style={styles.dot('#fb7185')} />
          <div style={styles.dot('#fbbf24')} />
          <div style={styles.dot('#4ade80')} />
          <div style={{marginLeft: 10}}>{title}</div>
        </div>
        <div>{terminal ? 'live demo' : 'code walkthrough'}</div>
      </div>
      <div style={styles.codeBody}>
        {lines.map((line, index) => {
          const reveal = interpolate(frame, [8 + index * 4, 14 + index * 4], [0.15, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const isActive = index === activeLine;
          const keyword = line.trim().startsWith('def') || line.trim().startsWith('if') || line.trim().startsWith('from');
          const command = terminal && line.trim().startsWith('python');

          return (
            <div
              key={`${title}-${index}-${line}`}
              style={{
                ...styles.codeLine,
                opacity: reveal,
                backgroundColor: isActive ? `${accent}18` : 'transparent',
                border: isActive ? `1px solid ${accent}55` : '1px solid transparent',
                transform: `translateX(${(1 - reveal) * 10}px)`,
              }}
            >
              <div style={styles.lineNumber}>{String(index + 1).padStart(2, '0')}</div>
              <div style={{color: command || keyword ? accent : '#dbeafe'}}>{line || ' '}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const SubtitleOverlay = () => {
  const frame = useCurrentFrame();
  const cue = subtitleTrack.find((item) => frame >= item.start && frame < item.end) || subtitleTrack[subtitleTrack.length - 1];

  if (!cue) {
    return null;
  }

  const opacity = interpolate(frame, [cue.start, cue.start + 8, cue.end - 8, cue.end], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const cueProgress = clamp((frame - cue.start) / (cue.end - cue.start), 0, 1);

  return (
    <div style={{...styles.subtitleShell, opacity}}>
      <div style={styles.subtitleBox}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12}}>
          <div style={{...styles.tag, padding: '8px 14px', fontSize: 18, color: '#f8fafc', borderColor: `${cue.accent}55`}}>
            <div style={styles.dot(cue.accent)} />
            配音字幕 / {cue.chapterLabel}
          </div>
          <div style={{fontSize: 18, color: textMuted}}>Cue {cue.cueIndex + 1}</div>
        </div>
        <div style={styles.subtitleText}>{cue.text}</div>
        <div
          style={{
            marginTop: 14,
            height: 5,
            borderRadius: 999,
            overflow: 'hidden',
            backgroundColor: 'rgba(148, 163, 184, 0.18)',
          }}
        >
          <div
            style={{
              width: `${cueProgress * 100}%`,
              height: '100%',
              background: `linear-gradient(90deg, ${cue.accent}, rgba(255, 255, 255, 0.92))`,
            }}
          />
        </div>
      </div>
    </div>
  );
};

const IntroScene = ({chapter}) => {
  return (
    <PageShell
      accent={chapter.accent}
      durationInFrames={chapter.durationInFrames}
      sceneIndex={chapter.sceneIndex}
      title="从文档到视频"
    >
      <div style={{...styles.sectionGrid, alignItems: 'center'}}>
        <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
          <div style={{...styles.eyebrow, color: introScene.accent}}>第一天教学视频</div>
          <div style={styles.heroTitle}>{day1Overview.title}</div>
          <div style={{...styles.heroSubtitle, color: '#7dd3fc'}}>{day1Overview.subtitle}</div>
          <div style={styles.heroText}>{day1Overview.goal}</div>
          <div style={{marginTop: 28, maxWidth: 520}}>
            <StatCards accent={chapter.accent} items={day1Overview.stats} />
          </div>
        </div>
        <div style={{display: 'grid', gap: 24}}>
          <div style={{...styles.panel, minHeight: 280, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <OrbitCluster
              accent={chapter.accent}
              centerLabel="文档\n拆成镜头"
              items={['README', 'hello.py', 'test.py', '配音稿', '字幕', '动画']}
            />
          </div>
        </div>
      </div>
      <div style={styles.footer}>
        <div>素材来源: `2026-04-16-day1` 文档和示例代码</div>
        <div>新增: 字幕节奏、中文配音稿、强化动画</div>
      </div>
    </PageShell>
  );
};

const ChecklistScene = ({chapter}) => {
  return (
    <PageShell
      accent={chapter.accent}
      durationInFrames={chapter.durationInFrames}
      sceneIndex={chapter.sceneIndex}
      title="先建立最小闭环"
    >
      <div style={styles.sectionGrid}>
        <div style={styles.panel}>
          <div style={{...styles.eyebrow, color: chapter.accent}}>Today&apos;s Roadmap</div>
          <div style={styles.sectionTitle}>Day 1 核心目标</div>
          <div style={styles.conceptText}>先把第一天最关键的 6 件事学明白，之后的内容都会轻松很多。</div>
          <BulletList accent={chapter.accent} items={checklistItems} />
        </div>
        <div style={{display: 'grid', gap: 24}}>
          <div style={{...styles.panel, minHeight: 320}}>
            <OrbitCluster
              accent={chapter.accent}
              centerLabel={checklistScene.callout}
              items={['变量', '函数', '模块', '容器', '循环', '入口']}
            />
          </div>
          <div style={{...styles.panel, ...styles.panelAlt}}>
            <div style={{...styles.eyebrow, color: '#bbf7d0'}}>为什么这样安排</div>
            <BulletList accent="#86efac" items={checklistScene.reasons} />
          </div>
        </div>
      </div>
    </PageShell>
  );
};

const SectionScene = ({chapter}) => {
  const {section} = chapter;

  return (
    <PageShell
      accent={chapter.accent}
      durationInFrames={chapter.durationInFrames}
      sceneIndex={chapter.sceneIndex}
      title={section.title}
    >
      <div style={styles.sectionGrid}>
        <div style={{...styles.panel, borderColor: `${section.accent}44`}}>
          <div style={{...styles.eyebrow, color: section.accent}}>README 拆解</div>
          <div style={styles.sectionTitle}>{section.title}</div>
          <div style={styles.conceptText}>{section.concept}</div>
          <BulletList accent={section.accent} items={section.points} />
          <ChipRow accent={section.accent} chips={section.chips} />
          <div style={{...styles.callout, marginTop: 24, borderColor: `${section.accent}44`}}>
            <div style={{fontSize: 22, color: textMuted, marginBottom: 8}}>讲解建议</div>
            <div style={{fontSize: 30, lineHeight: 1.45}}>先解释概念，再对照代码，再用一句话点明它在后端里的真实用途。</div>
          </div>
        </div>
        <CodePanel accent={section.accent} lines={section.code} title="hello.py" />
      </div>
      <div style={styles.footer}>
        <div>Scene {chapter.sceneIndex + 1}</div>
        <div>字幕和代码高亮按讲解节奏推进</div>
      </div>
    </PageShell>
  );
};

const RunScene = ({chapter}) => {
  return (
    <PageShell
      accent={chapter.accent}
      durationInFrames={chapter.durationInFrames}
      sceneIndex={chapter.sceneIndex}
      title="把它真正跑起来"
    >
      <div style={styles.sectionGrid}>
        <div style={styles.panel}>
          <div style={{...styles.eyebrow, color: chapter.accent}}>Run Demo</div>
          <div style={styles.sectionTitle}>怎么运行 Day 1 示例</div>
          <div style={styles.conceptText}>教学视频里，这一段最适合配终端画面或者命令演示。</div>
          <BulletList accent="#fbbf24" items={runScene.steps} />
          <div style={{...styles.callout, marginTop: 26}}>
            <div style={{fontSize: 22, color: textMuted, marginBottom: 10}}>重点提醒</div>
            <div style={{fontSize: 30, lineHeight: 1.45}}>如果学员能独立执行 `python hello.py` 并看懂输出，Day 1 就真正落地了。</div>
          </div>
        </div>
        <CodePanel accent="#fbbf24" lines={runScene.terminalLines} terminal title="terminal" />
      </div>
    </PageShell>
  );
};

const SummaryScene = ({chapter}) => {
  return (
    <PageShell
      accent={chapter.accent}
      durationInFrames={chapter.durationInFrames}
      sceneIndex={chapter.sceneIndex}
      title="结尾总结和练习"
    >
      <div style={styles.sectionGrid}>
        <div style={styles.panel}>
          <div style={{...styles.eyebrow, color: chapter.accent}}>Completion Check</div>
          <div style={styles.sectionTitle}>今天学完后的标准</div>
          <BulletList accent="#c4b5fd" items={summaryScene.completionItems} />
        </div>
        <div style={{display: 'grid', gap: 24}}>
          <div style={styles.panel}>
            <div style={{...styles.eyebrow, color: '#f9a8d4'}}>Practice</div>
            <div style={{fontSize: 42, fontWeight: 800, marginBottom: 16}}>建议再练 3 个小改动</div>
            <BulletList accent="#f9a8d4" items={summaryScene.practiceItems} />
          </div>
          <div style={{...styles.panel, backgroundColor: '#0f172a', borderColor: `${chapter.accent}44`}}>
            <div style={{fontSize: 22, color: textMuted, marginBottom: 10}}>下一步</div>
            <div style={{fontSize: 40, fontWeight: 800, lineHeight: 1.3}}>{summaryScene.nextStep}</div>
          </div>
        </div>
      </div>
    </PageShell>
  );
};

export const Day1Video = () => {
  return (
    <AbsoluteFill>
      {chapterTimeline.map((chapter) => {
        let component = null;

        if (chapter.kind === 'intro') {
          component = <IntroScene chapter={chapter} />;
        }

        if (chapter.kind === 'checklist') {
          component = <ChecklistScene chapter={chapter} />;
        }

        if (chapter.kind === 'section') {
          component = <SectionScene chapter={chapter} />;
        }

        if (chapter.kind === 'run') {
          component = <RunScene chapter={chapter} />;
        }

        if (chapter.kind === 'summary') {
          component = <SummaryScene chapter={chapter} />;
        }

        return (
          <Sequence key={chapter.key} durationInFrames={chapter.durationInFrames} from={chapter.start}>
            {component}
          </Sequence>
        );
      })}

      {/* 字幕条放在最上层，用全局时间轴查当前应该显示哪一句。 */}
      <SubtitleOverlay />
    </AbsoluteFill>
  );
};
