def calculate_progress_datetime(
    start_time,
    end_time,
    current_time,
    length: int = 20,
    fill_char: str = "█",
    empty_char: str = "░",
) -> str:
    total_duration = end_time - start_time
    elapsed_duration = current_time - start_time

    progress_percentage = min(100, max(0, (elapsed_duration / total_duration) * 100))
    progress_bar = int(progress_percentage / 100 * length)

    progress_string = f"[{fill_char * progress_bar}{empty_char * (length - progress_bar)}] {progress_percentage:.2f}%"
    return progress_string


def calculate_digit_progress(
    start,
    end,
    current,
    length: int = 20,
    fill_char: str = "█",
    empty_char: str = "░",
) -> str:
    progress_percentage = min(100, max(0, (current - start) / (end - start) * 100))
    progress_bar = int(progress_percentage / 100 * length)

    progress_string = f"[{fill_char * progress_bar}{empty_char * (length - progress_bar)}] {progress_percentage:.2f}%"
    return progress_string