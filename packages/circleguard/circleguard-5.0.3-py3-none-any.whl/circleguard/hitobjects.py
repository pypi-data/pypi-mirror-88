import numpy as np
from slider.beatmap import Circle as SliderCircle
from slider.beatmap import Slider as SliderSlider
from slider.beatmap import Spinner as SliderSpinner
from slider.mod import circle_radius

# We define our own hitobjects as the slider library's hitobjects have too many
# attributes and methods we don't care about, and they also lock position
# behind an extra attribute access (``hitobj.position.x``` vs ``hitobj.x``)
# which I'm not a fan of.
# Another necessary change is our hitobjects are "replay/map aware", which means
# they know how large they are (or potentially how difficult they are to hit
# as a result of OD if that is necessary in the future) because we know with
# what mods and on what map the hitobject was played with.

class Hitobject():
    """
    A Hitobject in osu! gameplay, with a time and a position.
    """
    def __init__(self, t, xy):
        self.t = t
        self.xy = xy
        self.x = xy[0]
        self.y = xy[1]

    @classmethod
    def from_slider_hitobj(self, hitobj, CS):
        """
        Instantiates a circleguard hitobject from a
        :class:`slider.beatmap.HitObject` and a circle size.
        """
        # convert to ms
        t = hitobj.time.total_seconds() * 1000

        xy = [hitobj.position.x, hitobj.position.y]
        xy = np.array(xy)

        radius = circle_radius(CS)

        if isinstance(hitobj, SliderCircle):
            return Circle(t, xy, radius)
        if isinstance(hitobj, SliderSlider):
            return Slider(t, xy, radius)
        if isinstance(hitobj, SliderSpinner):
            return Spinner(t, xy)

    def __eq__(self, other):
        return self.t == other.t and self.xy == other.xy

    def __hash__(self):
        return hash((self.t, self.xy))


class Circle(Hitobject):
    """
    A circle in osu! gameplay, with a time, position, and radius.
    """
    def __init__(self, time, xy, radius):
        super().__init__(time, xy)
        self.radius = radius

    def __eq__(self, other):
        return (self.t == other.t and self.xy == other.xy and
            self.radius == other.radius)

    def __hash__(self):
        return hash((self.t, self.xy, self.radius))


class Slider(Hitobject):
    """
    A slider in osu! gameplay, with a time, position, and radius.
    """
    def __init__(self, time, xy, radius):
        super().__init__(time, xy)
        self.radius = radius

    def __eq__(self, other):
        return (self.t == other.t and self.xy == other.xy and
            self.radius == other.radius)

    def __hash__(self):
        return hash((self.t, self.xy, self.radius))


class Spinner(Hitobject):
    """
    A spinner in osu! gameplay, with a time and position.
    """
    def __init__(self, time, xy):
        super().__init__(time, xy)
