// import React from "react";
import React, { useState } from "react";
import { Link } from "react-router-dom";

import "./HomePage.css";

// function App() {
export default function HomePage() {
  return (
    <div className="main-bg">
      {/* 第一部分 */}
      {/* <header className="header">
        <div className="logo">
          {" "}
          <img
            src="https://static.wegic.com/logo.svg"
            alt="logo"
            className="logo-img"
          />{" "}
        </div>
        <nav className="nav">首页</nav>
      </header> */}
      <section className="section section-yellow">
        <h2 className="section-title-green">雅思写作，从这里开始提升</h2>
        <p className="section-desc">
          我们提供最佳的学习资源和工具，素材生成、评分服务、范文参考，综合提升您的写作能力。
        </p>
        <div className="card-group">
          <div className="card">
            <img
              src="https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=400&q=80"
              alt="每日精读"
              className="card-img"
            />
            <div className="card-content">
              <h3>每日精读</h3>
              <p>优质素材，稳步进步</p>
              {/* <button>点击进入</button> */}
              <Link to="/material">
                <button>点击进入</button>
              </Link>
            </div>
          </div>
          <div className="card">
            <img
              src="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=400&q=80"
              alt="小练身手"
              className="card-img"
            />
            <div className="card-content">
              <h3>小练身手</h3>
              <p>智能出题，灵活运用</p>
              {/* <button>点击进入</button> */}
              <Link to="/polish">
                <button>点击进入</button>
              </Link>
            </div>
          </div>
          <div className="card">
            <img
              src="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=400&q=80"
              alt="实战演练"
              className="card-img"
            />
            <div className="card-content">
              <h3>实战演练</h3>
              <p>模拟考试，循序渐进</p>
              {/* <button>点击进入</button> */}
              <Link to="/practice">
                <button>点击进入</button>
              </Link>
            </div>
          </div>
        </div>
        {/* <div className="made-in-wegic">Made in Wegic</div> */}
      </section>

      {/* 第二部分 */}
      <section className="section section-green">
        <h2 className="section-title">轻松掌握雅思写作，只需简单几步</h2>
        <p className="section-desc">
          我们的智能分析系统将帮助您快速发现写作问题，并提供针对性的改进建议和学习资源。
        </p>
        <div className="steps">
          <div className="step">
            <div className="step-icon">📝</div>
            <div>
              <h4>提交您的作文</h4>
              <p>输入您的英语作文，我们将为您提供专业的分析和改进建议。</p>
            </div>
          </div>
          <div className="step">
            <div className="step-icon">🔍</div>
            <div>
              <h4>智能分析</h4>
              <p>系统将分析您的作文，识别语法、词汇、逻辑等方面的问题，并提供详细的改进建议。</p>
            </div>
          </div>
          <div className="step">
            <div className="step-icon">📚</div>
            <div>
              <h4>获取学习材料</h4>
              <p>根据您的作文分析结果，系统会推荐针对性的学习材料，帮助您提升写作水平。</p>
            </div>
          </div>
        </div>
      </section>
      {/* 底部大横幅 */}
      <footer className="homepage-footer">
        <div className="footer-col left">
          <div className="footer-welcome">欢迎来到雅思写作提升站</div>
          <div className="footer-title">有兴趣一起提升写作水平吗？</div>
          <div className="footer-time">周一至周五， 9:00 am 至 6:00 pm</div>
          <div className="footer-desc">我们的团队随时为您解答疑问。</div>
        </div>
        <div className="footer-col center">
          <div className="footer-label">给我们留言</div>
          <div className="footer-email">support@example.com</div>
        </div>
        <div className="footer-col right">
          <div className="footer-label">FOLLOW US</div>
          <div className="footer-links">
            <div>
              <a href="#" target="_blank" rel="noopener noreferrer">
                Instagram
              </a>
            </div>
            <div>
              <a href="#" target="_blank" rel="noopener noreferrer">
                Facebook
              </a>
            </div>
            <div>
              <a href="#" target="_blank" rel="noopener noreferrer">
                LinkedIn
              </a>
            </div>
            <div>
              <a href="#" target="_blank" rel="noopener noreferrer">
                Medium
              </a>
            </div>
            <div>
              <a href="#" target="_blank" rel="noopener noreferrer">
                Behance
              </a>
            </div>
            <div>
              <a href="#" target="_blank" rel="noopener noreferrer">
                Dribbble
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
