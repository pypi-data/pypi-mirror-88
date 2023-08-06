import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PlotWCA(object):
    '''
    Plots related to WCA Config Delivery
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def plotMaxSafeTable(self, outputName, maxSafeTable, limit, title, show = False):
        '''
        Plot the contents of the WCA MaxSafePowerTable
        :param outputName: PNG file to write
        :param maxSafeTable: list of dict{freqLO, yigTuning, VD0, VD1, power0, power1}
                            sorted by freqLO
        :param limit: maximum output power spec limit in mW
        :param title: plot title to display
        :param show: if True, display the plot interactively
        '''
        if not maxSafeTable:
            return
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        x = [row['freqLO'] for row in maxSafeTable]
        VD0 = [row['VD0'] for row in maxSafeTable]
        VD1 = [row['VD1'] for row in maxSafeTable]
        power0 = [row['power0'] for row in maxSafeTable]
        power1 = [row['power1'] for row in maxSafeTable]
        limitX = [x[0], x[-1]]
        limitY = [limit, limit]
        line0 = dict(color='firebrick', width=4)
        line1 = dict(color='royalblue', width=4)
        line2 = dict(color='black', width=1)                     
        fig.add_trace(go.Scatter(x = x, y = power0, line = line0, name = 'power0'), secondary_y=False)
        fig.add_trace(go.Scatter(x = x, y = power1, line = line1, name = 'power1'), secondary_y=False)
        fig.add_trace(go.Scatter(x = limitX, y = limitY, line = line2, name = 'limit', mode='lines'), secondary_y=False)
        line0['dash'] = 'dash'                    
        line1['dash'] = 'dash'
        fig.add_trace(go.Scatter(x = x, y = VD0, line = line0, name = 'VD0 set'), secondary_y=True)
        fig.add_trace(go.Scatter(x = x, y = VD1, line = line1, name = 'VD1 set'), secondary_y=True)
        fig.update_xaxes(title_text = 'freqLO [GHz]')
        fig.update_yaxes(title_text = 'power0, power1 [mW]', secondary_y=False)
        fig.update_yaxes(title_text = 'VD0, VD1', secondary_y=True)
        # yrange is limit rounded up to the next multiple of 50:
        yrange = limit + (50 - limit % 50) if (limit % 50) else limit                    
        fig.update_yaxes(range=[0, yrange], secondary_y=False)
        fig.update_yaxes(range=[0, 3], secondary_y=True)
        fig.update_layout(title_text = title)
        
        imageData = fig.to_image(format = "png", width = 800, height = 500)
        # save to file, if requested:
        if outputName:
            with open(outputName, 'wb') as file:
                file.write(imageData)
        # show interactive:
        if show:
            fig.show()
