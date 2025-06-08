import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getIeltsQuestion } from "./api/ieltsPractice";
import "./PracticeList.css";

// 生成剑雅19~剑雅10
const books = Array.from({ length: 10 }, (_, i) => `剑雅${19 - i}`);
const tests = [1, 2, 3, 4];

export default function PracticeList() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentBook, setCurrentBook] = useState(books[0]);

  const handleTestClick = async (book, test) => {
    try {
      setLoading(true);
      setError(null);
      // 获取指定版本和测试的题目
      const response = await getIeltsQuestion(book, `TEST${test}`);
      if (response.success && response.data) {
        // 从"剑雅10"中提取"10"
        const bookId = book.replace("剑雅", "");
        navigate(`/practice/${bookId}/${test}`, { 
          state: { 
            question: response.data,
            bookId,
            testId: test
          } 
        });
      } else {
        setError(response.error || '获取题目失败');
      }
    } catch (error) {
      console.error('获取题目失败:', error);
      setError(error.message || '获取题目失败');
    } finally {
      setLoading(false);
    }
  };

  const handleBookClick = (book) => {
    setCurrentBook(book);
  };

  if (loading) {
    return <div className="loading">加载中...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>错误: {error}</p>
        <button onClick={() => window.location.reload()}>重试</button>
      </div>
    );
  }

  return (
    <div className="practice-list-page">
      <div className="practice-list-header">
        <button className="back-btn" onClick={() => navigate("/")}>
          ⟵
        </button>
        <span>实战演练</span>
      </div>
      <div className="practice-list-content">
        <div className="practice-list-table">
          {books.map((book, idx) => (
            <div className="practice-list-row" key={book}>
              <div 
                className={`practice-list-book ${currentBook === book ? 'active' : ''}`}
                onClick={() => handleBookClick(book)}
              >
                {book}
              </div>
              {tests.map((test) => (
                <button
                  className="practice-list-test"
                  key={test}
                  onClick={() => handleTestClick(book, test)}
                >
                  Test {test}
                </button>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
