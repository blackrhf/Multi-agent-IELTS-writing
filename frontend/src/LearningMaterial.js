import React, { useState, useEffect } from "react";
import "./LearningMaterial.css";
import { useNavigate } from "react-router-dom";

// 默认文章（当没有用户作文时使用）
const defaultEssay = {
  title: "The Impact of Technology on Modern Education",
  content: `Technology has revolutionized the way we learn and teach in modern education. With the advent of digital tools and online platforms, education has become more accessible and interactive than ever before.

One of the most significant benefits of technology in education is its ability to make learning more engaging. Interactive whiteboards, educational apps, and online simulations allow students to visualize complex concepts and participate actively in their learning process. For instance, virtual reality can transport students to historical sites or scientific laboratories, creating immersive learning experiences that were previously impossible.

However, this technological transformation also presents challenges. The digital divide remains a significant issue, with many students lacking access to necessary devices and internet connectivity. Additionally, there are concerns about screen time and its impact on students' attention spans and social development.

Despite these challenges, the integration of technology in education is inevitable and largely beneficial. It prepares students for a digital future while making learning more efficient and engaging. The key is to find the right balance between traditional teaching methods and technological innovations.`,
  value: "探讨科技对教育的影响，包含利弊分析，适合学习议论文写作结构。",
  difficulty: "中等",
};

export default function LearningMaterial() {
  const navigate = useNavigate();
  const [material, setMaterial] = useState(defaultEssay);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const analyzeEssay = async () => {
      try {
        // 从localStorage获取用户作文
        const userEssay = localStorage.getItem('userEssay');
        
        if (userEssay) {
          setLoading(true);
          // 调用后端API分析作文
          const response = await fetch('http://localhost:5000/api/essay/analyze', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ essay: userEssay }),
          });

          if (!response.ok) {
            throw new Error('分析作文失败');
          }

          const data = await response.json();
          if (data.success) {
            setMaterial({
              title: data.material.title,
              content: data.material.content,
              value: data.material.learning_value,
              difficulty: data.material.difficulty,
            });
          } else {
            throw new Error(data.error || '分析作文失败');
          }
        }
      } catch (err) {
        setError(err.message);
        console.error('分析作文时出错:', err);
      } finally {
        setLoading(false);
      }
    };

    analyzeEssay();
  }, []);

  return (
    <div className="learning-material-page">
      <div className="learning-material-header">
        <button className="back-btn" onClick={() => navigate("/")}>
          ⟵
        </button>
        <span>每日精读</span>
      </div>
      <div className="learning-material-body">
        <div className="learning-material-left">
          <div className="material-card">
            {loading ? (
              <div className="loading">正在分析作文...</div>
            ) : error ? (
              <div className="error-message">{error}</div>
            ) : (
              <>
                <div className="material-title">{material.title}</div>
                <div className="material-meta">
                  <span>难度：{material.difficulty}</span>
                </div>
                <div className="material-content">{material.content}</div>
                <div className="material-value">
                  <b>重点学习价值：</b>
                  {material.value}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
