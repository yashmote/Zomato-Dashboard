# Zomato Bangalore Restaurant Analysis

This project explores restaurant data from Bangalore to understand what actually drives restaurant success — and more importantly, how someone could use that data to make better business decisions.

Instead of just plotting graphs, the goal here was to answer practical questions like:
- Where should I open a restaurant?
- What kind of pricing works best?
- Does online ordering actually matter?

---

## 🔗 Live App

[Live Dashboard](https://zomato-dashboard-ac5yby75yynmw3xmz7hvss.streamlit.app/)

---

## 💡 What this project does

I built an interactive dashboard using Streamlit where you can:

- Filter restaurants by location, cuisine, and online ordering
- Explore how ratings change across different segments
- See which areas are crowded vs underserved
- Get a clear recommendation for opening a new restaurant

---

## 📊 Key takeaways

Here are a few things that stood out from the analysis:

- Restaurants with online ordering tend to have slightly higher ratings (~0.2 difference), but it’s not a huge factor
- Mid-range pricing (₹400–₹800) performs the most consistently across locations
- Expensive restaurants don’t necessarily get better ratings
- Some locations have good ratings but fewer restaurants → potential opportunity
- Certain cuisines are highly rated but not very common → underserved niches

---

## 🧠 How the recommendation works

I built a simple scoring model based on three things:

- **Demand** → average rating  
- **Competition** → number of restaurants  
- **Pricing** → affordability  

The idea is:

> High rating + low competition + reasonable pricing = good opportunity

The dashboard uses this to suggest:
- Best location
- Best cuisine
- Ideal pricing range
- Expected rating

---

## 🔬 Analysis approach

- Cleaned the dataset (handled missing values, converted types)
- Created price categories (budget, mid-range, premium)
- Broke down cuisines for deeper analysis
- Used correlation and hypothesis testing to validate patterns
- Compared different segments (location, pricing, ordering)

---

## 📦 Dataset

- Source: Zomato Bangalore dataset from Kaggle  
- For deployment, I used a smaller compressed sample (~10k rows) so the app loads quickly

---

## ⚠️ Limitations

- The dataset is static (not real-time)
- Ratings are subjective
- No time-based trends available
- Competition is measured by count, not actual demand or revenue

---

## 🛠 Tech used

- Python (Pandas, NumPy)
- Seaborn & Matplotlib
- Streamlit (for the dashboard)
- SciPy (for hypothesis testing)

---

## 🎯 Final thought

This project was less about “making charts” and more about thinking:

> If I were actually opening a restaurant, what decisions would I make using this data?

---

## 👤 Author

Nihal
