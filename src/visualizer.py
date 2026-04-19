import matplotlib.pyplot as plt
from .config import EMOTION_COLORS
from .config import EMOTION_EMOJIS

def get_emotion_color(emotion):
    # Get color for emotion
    return EMOTION_COLORS.get(emotion, '#666666')


def get_emotion_emoji(emotion):
    # Get emoji for emotion
    return EMOTION_EMOJIS.get(emotion, '❓')


def plot_confidence_scores(probabilities, title="Emotion Confidence Distribution"):
    # Create bar chart with emotions on X-axis, confidence on Y-axis
    
    sorted_items = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    emotions = [item[0].title() for item in sorted_items]
    scores = [item[1] * 100 for item in sorted_items]
    colors = [get_emotion_color(item[0]) for item in sorted_items]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(emotions, scores, color=colors, edgecolor='white', linewidth=2)
    
    ax.set_xlabel('Emotion', fontsize=12, fontweight='bold')
    ax.set_ylabel('Confidence Score (%)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    return fig