
class Plotter:
  def __init__(self, is_matplotlib):
    self._is_matplotlib = is_matplotlib
    if self._is_matplotlib:
      pass

  def setPlotlyFunctions(self, setXandY, setTraceName=None, setColor=None):
    self._plotlySetXandY = setXandY
    self._plotlySetTraceName = setTraceName
    self._plotlySetColor = setColor

  def setMatplotlibAxis(self, axis):
    self._matplotlib_axis = axis

  def plot2D(self, x, y, color=None, label=None):
    if self._is_matplotlib:
      self._matplotlib_axis.plot(x, y, color=color, label=label)
    else:
      self._plotlySetXandY(x, y)
      if self._plotlySetColor: self._plotlySetColor(color)
      if self._plotlySetTraceName: self._plotlySetTraceName(label)

