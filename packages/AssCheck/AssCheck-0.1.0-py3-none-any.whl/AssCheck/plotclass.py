class line:
    def __init__(self, xdata, ydata, linestyle=None, colour=None,label=None,marker=None):
        self.xdata = xdata
        self.ydata = ydata
        self.linestyle= linestyle
        self.colour= colour
        self.label= label
        self.marker= marker
    def get_xydata(self):
        return(self.xdata,self.ydata)

