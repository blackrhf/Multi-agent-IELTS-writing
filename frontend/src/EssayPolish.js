import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getEssayQuestion, polishEssay } from "./api/essayPolish";
import "./EssayPolish.css";

const MAX_CHAR = 5000;
const MIN_WORDS = 250;

function countWords(text) {
  return (text.trim().match(/\b\w+\b/g) || []).length;
}

// 解析润色结果
function parsePolishResult(result) {
  const sections = {
    scores: [],
    essay: "",
    points: [],
    suggestions: []
  };

  const lines = result.split('\n');
  let currentSection = null;

  for (let line of lines) {
    line = line.trim();
    if (!line) continue;

    if (line === "评分分析") {
      currentSection = "scores";
      continue;
    } else if (line === "优化范文") {
      currentSection = "essay";
      continue;
    } else if (line === "修改要点") {
      currentSection = "points";
      continue;
    } else if (line === "建议论证方向") {
      currentSection = "suggestions";
      continue;
    }

    switch (currentSection) {
      case "scores":
        if (line.match(/^\d\./)) {
          sections.scores.push(line);
        }
        break;
      case "essay":
        sections.essay += line + "\n";
        break;
      case "points":
        if (line.match(/^\d\./)) {
          sections.points.push(line);
        }
        break;
      case "suggestions":
        if (line.startsWith("-")) {
          sections.suggestions.push(line.substring(1).trim());
        }
        break;
    }
  }

  return sections;
}

export default function EssayPolish() {
  const [question, setQuestion] = useState("");
  const [essay, setEssay] = useState("");
  const [polished, setPolished] = useState(null);
  const [showPolished, setShowPolished] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const charCount = essay.length;
  const wordCount = countWords(essay);

  useEffect(() => {
    fetchQuestion();
  }, []);

  async function fetchQuestion() {
    try {
      setLoading(true);
      const response = await getEssayQuestion();
      if (response.success) {
        setQuestion(response.question);
      } else {
        setError('获取题目失败');
      }
    } catch (err) {
      setError('获取题目失败: ' + err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handlePolish() {
    if (!essay.trim()) {
      setError('请输入文章内容');
      return;
    }

    try {
      setLoading(true);
      const response = await polishEssay(essay);
      if (response.success) {
        setPolished(parsePolishResult(response.polishedEssay));
        setShowPolished(true);
      } else {
        setError('润色失败');
      }
    } catch (err) {
      setError('润色失败: ' + err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleChange(e) {
    if (e.target.value.length <= MAX_CHAR) {
      setEssay(e.target.value);
    }
  }

  const handleSubmit = async () => {
    if (!essay.trim()) {
      setError("请输入作文内容");
      return;
    }

    if (essay.trim().length < 50) {
      setError("作文内容太短，请至少输入50个单词");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // 保存作文到localStorage
      localStorage.setItem('userEssay', essay);
      
      const response = await fetch('http://localhost:5000/api/essay/polish', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ essay }),
      });

      if (!response.ok) {
        throw new Error('润色失败');
      }

      const data = await response.json();
      if (data.success) {
        navigate('/polish/result', {
          state: {
            originalEssay: essay,
            polishedEssay: data.polishedEssay
          }
        });
      } else {
        throw new Error(data.error || '润色失败');
      }
    } catch (error) {
      console.error('润色作文失败:', error);
      setError(error.message || '润色失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="essay-polish-page">
      {/* Header */}
      <div className="essay-polish-header">
        <button className="back-btn" onClick={() => navigate("/")}>
          ⟵
        </button>
        {/* <span>小练身手</span> */}
      </div>
      {/* Body */}
      <div className="essay-content-center">
        {/* A: 题目 */}
        <div className="essay-question">
          {loading ? '加载中...' : question}
        </div>
        {error && <div className="error-message">{error}</div>}
        {/* B: 一键润色按钮 */}
        {!showPolished && (
          <div className="polish-btn-row">
            <button 
              className="polish-btn-center" 
              onClick={handleSubmit}
              disabled={loading || !essay.trim()}
            >
              {loading ? '处理中...' : '一键润色'}
            </button>
          </div>
        )}
        {/* C: 输入栏和润色栏 */}
        <div className="essay-main-columns">
          <div className={`essay-input-area ${showPolished ? "half" : "wide"}`}>
            {!showPolished ? (
              <div className="textarea-wrapper">
                <textarea
                  className="essay-input"
                  placeholder="请在此输入你的作文..."
                  value={essay}
                  onChange={handleChange}
                  rows={12}
                  disabled={showPolished || loading}
                />
                <div className="essay-word-count-float">
                  characters: {charCount}/{MAX_CHAR} | words: {wordCount}
                  {wordCount < MIN_WORDS ? `（建议不少于${MIN_WORDS}词）` : ""}
                </div>
              </div>
            ) : (
              <div className="original-essay">{essay}</div>
            )}
          </div>
          <div className={`essay-polished-area ${showPolished ? "half" : "narrow"}`}>
            {showPolished && polished ? (
              <div className="essay-polished-content">
                <div className="polish-section">
                  <h3>评分分析</h3>
                  {polished.scores.map((score, index) => (
                    <div key={index} className="score-item">{score}</div>
                  ))}
                </div>
                <div className="polish-section">
                  <h3>优化范文</h3>
                  <div className="polished-essay">{polished.essay}</div>
                </div>
                <div className="polish-section">
                  <h3>修改要点</h3>
                  {polished.points.map((point, index) => (
                    <div key={index} className="point-item">{point}</div>
                  ))}
                </div>
                <div className="polish-section">
                  <h3>建议论证方向</h3>
                  {polished.suggestions.map((suggestion, index) => (
                    <div key={index} className="suggestion-item">• {suggestion}</div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="essay-polished-placeholder">
                润色结果将在此显示
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
