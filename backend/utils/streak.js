const IST_TIMEZONE = 'Asia/Kolkata';

export const updateStreak = (user) => {
    const today = getDateInIST(new Date());

    // First login ever
    if (!user.lastActiveDate) {
        user.currentStreak = 1;
        user.longestStreak = 1;
        user.lastActiveDate = new Date();
        return true;
    }

    const lastActiveDay = getDateInIST(user.lastActiveDate);

    // Already logged in today
    if (today === lastActiveDay) {
        return false;
    }

    const differenceInDays = getDateDifference(
        lastActiveDay,
        today
    );

    if (differenceInDays === 1) {
        user.currentStreak += 1;
    } else {
        user.currentStreak = 1;
    }

    if (user.currentStreak > user.longestStreak) {
        user.longestStreak = user.currentStreak;
    }

    user.lastActiveDate = new Date();

    return true;
};

const getDateInIST = (date) => {
    return new Intl.DateTimeFormat('en-CA', {
        timeZone: IST_TIMEZONE,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).format(date);
};

const getDateDifference = (oldDate, newDate) => {
    const oldTime = new Date(`${oldDate}T00:00:00Z`);
    const newTime = new Date(`${newDate}T00:00:00Z`);

    return Math.round(
        (newTime - oldTime) / (1000 * 60 * 60 * 24)
    );
};