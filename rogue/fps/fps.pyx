# cython: languagelevel=3

from libc.time cimport clock, clock_t, CLOCKS_PER_SEC

cdef enum: FRAMES_TO_AVG = 20

cdef class Fps:
    cdef int i
    cdef int counter
    cdef float frame_times[FRAMES_TO_AVG]
    cdef clock_t start, end
    cdef float time_taken, fps

    def __init__(self):
        for i in range(FRAMES_TO_AVG):
            self.frame_times[i] = 60
            self.start = clock()

    cdef _tick(self):
        cdef int j

        self.end = clock()
        self.time_taken = <float>(self.end - self.start) / (CLOCKS_PER_SEC);
        self.start = self.end
        self.frame_times[self.counter] = self.time_taken
        self.counter += 1

        if self.counter >= FRAMES_TO_AVG:
            self.counter = 0

        self.fps = 0.0
        for j in range(FRAMES_TO_AVG):
            self.fps += self.frame_times[j]

        self.fps = FRAMES_TO_AVG / self.fps

    def tick(self):
        self._tick()

    def current(self):
        return self.fps