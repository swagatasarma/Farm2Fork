
def get_recommendations(energy):
    tips = []
    if energy > 5:
        tips.append("Consider using solar-powered irrigation to reduce energy use.")
    if energy > 8:
        tips.append("High energy usage detected. Check for equipment inefficiencies.")
    if energy < 2:
        tips.append("Excellent! Low energy usage. Keep it up.")
    return tips
