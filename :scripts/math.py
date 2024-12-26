import numpy as num
import matplotlib


class DisGUI():
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data

        self.frames = []
        self.framesCol = 0
        self.framesRow = 4
        self.totalframes = 0

        self.figs = []

        self.ControlFrames = []

        self.ChannelFrame = []

        self.ViewVar = []
        self.OptionVar = []
        self.FunVar = []

    def AddChannelMaster(self):
        self.AddMasterFrame()
        self.AdjustRootFrame()
        self.AddGraph()
        self.AddChannelFrame()
        self.AddBtnFrame()

    def AddMasterFrame(self):
        self.frames.append(LabelFrame(
            self.root, text=f"Display Manager - {len(self.frames)+1}", padx=5, pady=5, bg="white"))
        self.totalframes = len(self.frames)-1

        if self.totalframes % 2 == 0:
            self.framesCol = 0
        else:
            self.framesCol = 9

        self.framesRow = 4 + 4 * int(self.totalframes/2)
        self.frames[self.totalframes].grid(
            padx=5, column=self.framesCol, row=self.framesRow, columnspan=9, sticky=NW)

    def AdjustRootFrame(self):
        self.totalframes = len(self.frames)-1
        if self.totalframes > 0:
            RootW = 800*2
        else:
            RootW = 800
        if self.totalframes+1 == 0:
            RootH = 120
        else:
            RootH = 120 + 430 * (int(self.totalframes/2)+1)
        self.root.geometry(f"{RootW}x{RootH}")

    def AddGraph(self):
        self.figs.append([])
        self.figs[self.totalframes].append(plt.Figure(figsize=(7, 5), dpi=80))

        self.figs[self.totalframes].append(
            self.figs[self.totalframes][0].add_subplot(111))

        self.figs[self.totalframes].append(
            FigureCanvasTkAgg(self.figs[self.totalframes][0], master=self.frames[self.totalframes]))

        self.figs[self.totalframes][2].get_tk_widget().grid(
            column=1, row=0, rowspan=17, columnspan=4, sticky=N)

    def AddBtnFrame(self):
        btnH = 2
        btnW = 4

        self.ControlFrames.append([])
        self.ControlFrames[self.totalframes].append(
            LabelFrame(self.frames[self.totalframes], pady=5, bg="white"))
        self.ControlFrames[self.totalframes][0].grid(
            column=0, row=0, padx=5, pady=5, sticky=N)
        self.ControlFrames[self.totalframes].append(
            Button(self.ControlFrames[self.totalframes][0], text="+", bg="white", width=btnW, height=btnH, command=partial(self.AddChannel, self.ChannelFrame[self.totalframes])))
        self.ControlFrames[self.totalframes][1].grid(
            column=0, row=0, padx=5, pady=5)
        self.ControlFrames[self.totalframes].append(
            Button(self.ControlFrames[self.totalframes][0], text="-", bg="white", width=btnW, height=btnH, command=partial(self.DeleteChannel, self.ChannelFrame[self.totalframes])))
        self.ControlFrames[self.totalframes][2].grid(
            column=1, row=0, padx=5, pady=5)

    def AddChannelFrame(self):
        '''
        Methods that adds the main frame that will manage the frames of the options

        '''
        self.ChannelFrame.append([])
        self.ViewVar.append([])
        self.OptionVar.append([])
        self.FunVar.append([])
        self.ChannelFrame[self.totalframes].append(LabelFrame(self.frames[self.totalframes],
                                                              pady=5, bg="white"))
        self.ChannelFrame[self.totalframes].append(self.totalframes)

        self.ChannelFrame[self.totalframes][0].grid(
            column=0, row=1, padx=5, pady=5, rowspan=16, sticky=N)

        self.AddChannel(self.ChannelFrame[self.totalframes])

    def AddChannel(self, ChannelFrame):
        '''
        Method that initiate the channel frame which will provide options & control to the user
        '''
        if len(ChannelFrame[0].winfo_children()) < 8:
            NewFrameChannel = LabelFrame(ChannelFrame[0], bg="white")
            # print(
            #     f"Mumber of element into the Frame {len(ChannelFrame.winfo_children())}")

            NewFrameChannel.grid(column=0, row=len(
                ChannelFrame[0].winfo_children())-1)

            self.ViewVar[ChannelFrame[1]].append(IntVar())
            Ch_btn = Checkbutton(NewFrameChannel, variable=self.ViewVar[ChannelFrame[1]][len(self.ViewVar[ChannelFrame[1]])-1],
                                 onvalue=1, offvalue=0, bg="white")
            Ch_btn.grid(row=0, column=0, padx=1)
            self.ChannelOption(NewFrameChannel, ChannelFrame[1])
            self.ChannelFunc(NewFrameChannel, ChannelFrame[1])

    def ChannelOption(self, Frame, ChannelFrameNumber):
        self.OptionVar[ChannelFrameNumber].append(StringVar())

        bds = self.data.Channels

        self.OptionVar[ChannelFrameNumber][len(
            self.OptionVar[ChannelFrameNumber])-1].set(bds[0])
        drop_ch = OptionMenu(Frame, self.OptionVar[ChannelFrameNumber][len(
            self.OptionVar[ChannelFrameNumber])-1], *bds)
        drop_ch.config(width=5)
        drop_ch.grid(row=0, column=1, padx=1)

    def ChannelFunc(self, Frame, ChannelFrameNumber):
        self.FunVar[ChannelFrameNumber].append(StringVar())

        bds = [func for func in self.data.FunctionMaster.keys()]

        self.FunVar[ChannelFrameNumber][len(
            self.OptionVar[ChannelFrameNumber])-1].set(bds[0])
        drop_ch = OptionMenu(Frame, self.FunVar[ChannelFrameNumber][len(
            self.OptionVar[ChannelFrameNumber])-1], *bds)
        drop_ch.config(width=5)
        drop_ch.grid(row=0, column=2, padx=1)

    def DeleteChannel(self, ChannelFrame):
        if len(ChannelFrame[0].winfo_children()) > 1:
            ChannelFrame[0].winfo_children()[len(
                ChannelFrame[0].winfo_children())-1].destroy()
            self.ViewVar[ChannelFrame[1]].pop()
            self.OptionVar[ChannelFrame[1]].pop()
            self.FunVar[ChannelFrame[1]].pop()

