import React from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { getSampleEssay } from "./api/ieltsPractice";
import "./PracticeResult.css";

export default function PracticeResult() {
  const navigate = useNavigate();
  const { bookId, testId } = useParams();
  const location = useLocation();
  // 兼容 polishedEssay 字段
  const { answer, evaluation, polishedEssay, question } = location.state || {};

  const handleSampleClick = async () => {
    try {
      const response = await getSampleEssay(`剑雅${bookId}`, `TEST${testId}`);
      if (response.success) {
        navigate(`/practice/${bookId}/${testId}/sample`, {
          state: {
            answer,
            evaluation,
            question,
            sampleEssay: response.data
          }
        });
      } else {
        console.error('获取范文失败:', response.error);
      }
    } catch (error) {
      console.error('获取范文失败:', error);
    }
  };

  if (!evaluation) {
    return <div className="loading">加载中...</div>;
  }

  const feedback = evaluation.feedback || {};
  const feedbackItems = {
    general: feedback.general || "暂无总体反馈",
    coherence: feedback.coherence || "暂无连贯性反馈",
    grammar: feedback.grammar || "暂无语法反馈",
    task: feedback.task || "暂无任务完成度反馈",
    vocabulary: feedback.vocabulary || "暂无词汇反馈"
  };
  // 优先 evaluation.polished_result，其次 polishedEssay
  let optimizedEssay = polishedEssay || "暂无润色结果";

  // 评分栏只用ielts_evaluator的分数
  const scores = evaluation.scores || {
    task_achievement: 0,
    coherence_cohesion: 0,
    lexical_resource: 0,
    grammatical_range: 0,
    overall: 0
  };

  return (
    <div className="practice-result-page">
      <div className="practice-result-header">
        <button className="back-btn" onClick={() => navigate(`/practice/${bookId}/${testId}`)}>⟵</button>
        <span>剑雅{bookId} - Test {testId}</span>
      </div>
      <div className="practice-result-body">
        <div className="practice-result-main">
          <div className="practice-result-question">{question}</div>
          <div className="practice-result-content">
            <div className="practice-result-left">
              <div className="practice-result-original">
                <h3>原始作文</h3>
                <p>{answer}</p>
              </div>
              <div className="evaluation-scores">
                <h4>评分详情</h4>
                <div className="score-item">
                  <span>任务完成:</span>
                  <span>{scores.task_achievement}</span>
                </div>
                <div className="score-item">
                  <span>连贯衔接:</span>
                  <span>{scores.coherence_cohesion}</span>
                </div>
                <div className="score-item">
                  <span>词汇资源:</span>
                  <span>{scores.lexical_resource}</span>
                </div>
                <div className="score-item">
                  <span>语法范围:</span>
                  <span>{scores.grammatical_range}</span>
                </div>
                <div className="score-item total">
                  <span>总分:</span>
                  <span>{scores.overall}</span>
                </div>
              </div>
              <div className="evaluation-feedback">
                <h4>详细反馈</h4>
                {Object.entries(feedbackItems).map(([key, value]) => (
                  <div key={key} className="feedback-item">
                    <h5>{key}:</h5>
                    <p>{typeof value === 'object' ? JSON.stringify(value) : value}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="practice-result-right">
              <div className="practice-result-ai">
                <h3>AI润色结果</h3>
                {optimizedEssay.split('\n').map((line, idx) => (
                  <p key={idx}>{line}</p>
                ))}
              </div>
            </div>
          </div>
          <button className="sample-btn" onClick={handleSampleClick}>查看范文</button>
        </div>
      </div>
    </div>
  );
}