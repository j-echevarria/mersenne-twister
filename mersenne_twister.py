import time

W, N, M, R = (32, 624, 397, 31)
A = 0x9908B0DF
U = 11
S, B = (7, 0x9D2C5680)
T, C = (15, 0xEFC60000)
L = 18
F = 1812433253

class MersenneTwister:

    def __init__(self, seed: int | None = None) -> None:
        """Initializes the PRNG.

        Args:
            Optional seed value.
        """
        self._index = 0
        self._state = [0] * N
        self.seed(seed)

    def seed(self, seed: int | None = None) -> None:
        """Initializes the internal state from a seed.
        If no seed is provided, time is used.

        Args:
            Optional seed value.
        """
        if seed is None:
            seed = time.time_ns()
        seed = self._uint32(seed)
        self._initialize_state(seed)
        self._twist()

    def _initialize_state(self, seed: int) -> None:
        """Initializes the internal state from a seed.

        Args:
            Seed value.
        """
        state = self._state
        state[0] = 19650218

        for i in range(1, N):
            prev = state[i - 1]
            x_i = F * (prev ^ (prev >> (W - 2))) + i
            state[i] = self._uint32(x_i)

        # Bit scrambling to improve pseudo-randomness
        i = 1
        for _ in range(N):
            prev = state[i - 1]
            x_i = 1664525 * (prev ^ (prev >> (W - 2)))
            x_i ^= state[i]
            x_i += seed
            state[i] = self._uint32(x_i)
            i += 1
            if i == N:
                state[0] = state[N - 1]
                i = 1

        for _ in range(N - 1):
            prev = state[i - 1]
            x_i = 1566083941 * (prev ^ (prev >> (W - 2)))
            x_i ^= state[i]
            x_i -= i
            state[i] = self._uint32(x_i)
            i += 1
            if i == N:
                state[0] = state[N - 1]
                i = 1

        # Ensure the initial state is not in the kernel
        # of the twist transformation
        state[0] = 1 << R

    @staticmethod
    def _uint32(number: int) -> int:
        """Keeps the lower 32 bits of a number,
        since Python integers can be arbitrarily large.

        Args:
            Input number.

        Returns:
            Number constrained to 32 bits.
        """
        return number & 0xFFFFFFFF

    def _twist(self) -> None:
        """Twists the internal state."""
        state = self._state
        # Upper W - R bits
        upper_mask = ((1 << (N - R)) - 1) << R
        # Lower R bits
        lower_mask = (1 << R) - 1
        for i in range(N):
            x = (state[i] & upper_mask) + (state[(i + 1) % N] & lower_mask)
            xa = x >> 1
            if x & 1:
                xa ^= A
            state[i] = state[(i + M) % N] ^ xa
        self._index = 0

    @staticmethod
    def _temper(x: int) -> int:
        """Tempers the output.

        Args:
            Unsigned 32-bit integer.

        Returns:
            Tempered unsigned 32-bit integer.
        """
        x ^= (x >> U)
        x ^= ((x << S) & B)
        x ^= ((x << T) & C)
        x ^= (x >> L)
        return x

    def _generate_uint32(self) -> int:
        """Generates an unsigned w-bit integer.

        Returns:
            Pseudo-random unsigned w-bit integer.
        """
        if self._index == N:
            self._twist()

        x = self._state[self._index]
        self._index += 1
        return self._temper(x)

    def random(self) -> float:
        """Generates the next floating-point number
        in the range [0,1) with 53-bit precision.

        Returns:
            Number in the range [0,1).
        """
        # Keep upper 27 bits
        a = self._generate_uint32() >> 5
        # Keep upper 26 bits
        b = self._generate_uint32() >> 6
        # 9007199254740992 = 2^53
        return ((a << 26) + b) / 9007199254740992
