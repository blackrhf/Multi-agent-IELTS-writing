import React, { useState } from "react";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import { evaluateEssay } from "./api/ieltsPractice";
import "./PracticeTest.css";

export default function PracticeTest() {
  const navigate = useNavigate();
  const { bookId, testId } = useParams();
  const location = useLocation();
  const [answer, setAnswer] = useState("");
  const [question, setQuestion] = useState(location.state?.question || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!answer.trim()) {
      setError("请输入作文内容");
      return;
    }

    if (answer.trim().length < 50) {
      setError("作文内容太短，请至少输入50个单词");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      console.log('正在提交作文...');
      
      // 保存作文到localStorage
      localStorage.setItem('userEssay', answer);
      
      const response = await evaluateEssay(answer, "Task 2", question);
      
      if (response.success) {
        console.log('提交成功，正在跳转...');
        if (!bookId || !testId) {
          setError("版本或测试号未找到，请返回重试");
          return;
        }
        
        navigate(`/practice/${bookId}/${testId}/result`, {
          state: {
            answer,
            evaluation: response.evaluation,
            polishedEssay: response.polishedEssay,
            question
          }
        });
      } else {
        setError(response.error || '评估失败，请稍后重试');
      }
    } catch (error) {
      console.error('提交作文失败:', error);
      setError(error.message || '提交失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="practice-test-page">
      <div className="practice-test-header">
        <button className="back-btn" onClick={() => navigate("/practice")}>⟵</button>
        <span>剑雅{bookId} - Test {testId}</span>
      </div>
      <div className="practice-test-body">
        <div className="practice-test-main">
          <div className="practice-test-question">{question}</div>
          <div className="practice-test-answer">
            <textarea
              placeholder="请输入您的作文（至少50个单词）"
              value={answer}
              onChange={e => setAnswer(e.target.value)}
              disabled={loading}
            />
            <div className="word-count">Word Count: {answer.split(/\s+/).filter(Boolean).length}</div>
          </div>
          {error && <div className="error-message">{error}</div>}
          <button 
            className="submit-btn" 
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? '提交中...' : '提交'}
          </button>
        </div>
      </div>
    </div>
  );
}