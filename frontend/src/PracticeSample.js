import React from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import "./PracticeSample.css";

export default function PracticeSample() {
  const navigate = useNavigate();
  const { bookId, testId } = useParams();
  const location = useLocation();
  const { answer, evaluation, question, sampleEssay } = location.state || {};

  if (!sampleEssay) {
    return <div>加载中...</div>;
  }

  return (
    <div className="practice-sample-page">
      <div className="practice-sample-header">
        <button className="back-btn" onClick={() => navigate(`/practice/${bookId}/${testId}/result`)}>⟵</button>
      </div>
      <div className="practice-sample-body">
        <div className="practice-sample-main">
          <div className="practice-sample-question">{question}</div>
          <div className="practice-sample-original">
            <h3>原始作文</h3>
            <p>{answer}</p>
            <div className="evaluation-scores">
              <h4>评分详情</h4>
              <p>任务完成: {evaluation?.scores?.task_achievement}</p>
              <p>连贯衔接: {evaluation?.scores?.coherence_cohesion}</p>
              <p>词汇资源: {evaluation?.scores?.lexical_resource}</p>
              <p>语法范围: {evaluation?.scores?.grammatical_range}</p>
              <p>总分: {evaluation?.scores?.overall}</p>
            </div>
          </div>
          <div className="practice-sample-sample">
            <h3>范文</h3>
            <p>{sampleEssay.sample_essay}</p>
          </div>
          <button className="end-btn" onClick={() => navigate("/practice")}>结束学习</button>
        </div>
      </div>
    </div>
  );
}