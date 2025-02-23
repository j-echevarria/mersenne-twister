import time


class MersenneTwister:
    _N: int = 624
    _M: int = 397
    _W: int = 32
    _LOWER_MASK: int = 0x7FFFFFFF  # Least significant 31 bits
    _UPPER_MASK: int = 0x80000000  # Most significant bit

    def __init__(self, seed: int | None = None) -> None:
        """
        Initializes the Mersenne Twister (MT19937) pseudo-random number generator.

        Args:
            seed (int | None): An optional seed value.
        """
        self._state = [0] * self._N
        self._index = self._N
        self.seed(seed)

    def seed(self, seed: int | None = None) -> None:
        """
        Initializes the internal state with a seed.

        If no seed is provided, the current system time is used.

        Args:
            seed (int | None): An optional seed value.
        """
        seed = self._uint32(seed if seed else time.time_ns())
        self._initialize_state(seed)

    def random(self) -> float:
        """
        Generates the next floating-point number in the range [0,1) with 53-bit resolution.

        Returns:
            float: A number in the range [0,1).
        """
        a = self._generate_uint32() >> 5  # Keep top 27 bits
        b = self._generate_uint32() >> 6  # Keep top 26 bits
        return ((a << 26) + b) / 9007199254740992  # 9007199254740992 = 2^53

    def _initialize_state(self, seed: int) -> None:
        """
        Initializes the internal state from a seed.

        Args:
            seed (int): The seed value.
        """
        state = self._state
        state[0] = 19650218

        for i in range(1, self._N):
            state[i] = self._uint32(1812433253 * (state[i - 1] ^ (state[i - 1] >> (self._W - 2))) + i)

        # Tempering to improve pseudo-randomness
        i = 1
        for _ in range(self._N):
            state[i] = self._uint32((state[i] ^ ((state[i - 1] ^ (state[i - 1] >> 30)) * 1664525)) + seed)
            i += 1
            if i == self._N:
                state[0] = state[self._N - 1]
                i = 1

        # Further tempering to improve pseudo-randomness
        for _ in range(self._N - 1):
            state[i] = self._uint32((state[i] ^ ((state[i - 1] ^ (state[i - 1] >> 30)) * 1566083941)) - i)
            i += 1
            if i == self._N:
                state[0] = state[self._N - 1]
                i = 1

        # Set the most significant bit to ensure a non-zero state
        state[0] = 0x80000000
        self._index = self._N

    def _twist(self) -> None:
        """
        Generates the next N values from the series x_i.
        """
        state = self._state
        for i in range(self._N):
            x = (state[i] & self._UPPER_MASK) + (state[(i + 1) % self._N] & self._LOWER_MASK)
            xa = x >> 1
            if x & 1:
                xa ^= 0x9908B0DF
            state[i] = state[(i + self._M) % self._N] ^ xa
        self._index = 0

    def _generate_uint32(self) -> int:
        """
        Generates an unsigned 32-bit integer.

        Returns:
            int: A pseudo-random unsigned 32-bit integer.
        """
        if self._index == self._N:
            self._twist()

        x = self._state[self._index]
        self._index += 1
        return self._temper(x)

    def _temper(self, x: int) -> int:
        """
        Applies a tempering transform to improve pseudo-randomness.

        Args:
            x (int): The raw unsigned 32-bit integer from the state array.

        Returns:
            int: The tempered unsigned 32-bit integer.
        """
        x ^= (x >> 11)
        x ^= ((x << 7) & 0x9D2C5680)
        x ^= ((x << 15) & 0xEFC60000)
        x ^= (x >> 18)
        return self._uint32(x)

    @staticmethod
    def _uint32(number: int) -> int:
        """
        Keeps the lower 32 bits of a number and discards anything beyond that.

        Simulates unsigned 32-bit integer behavior in Python (since Python integers can be arbitrarily large).

        Args:
            number (int): The input number.

        Returns:
            int: The number constrained to 32 bits.
        """
        return number & 0xFFFFFFFF
