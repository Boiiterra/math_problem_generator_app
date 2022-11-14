def scale(width: int, height: int) -> float:
    if width / 950 <= height / 650 <= (width / 950) * 1.3 or height / 650 <= width / 950 <= (height / 650) * 1.3:
        return ((width / 950) + (height / 650)) / 2
    else:
        if height > width:
            return width / 950
        else:
            return height / 650
