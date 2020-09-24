import pandas as pd


if __name__ == "__main__":
    data = pd.read_csv(r"data\phone_records.csv", sep=";")
else:
    data = pd.read_csv(r"src\data\phone_records.csv", sep=";")


class Abonnent:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        if self.phone_number not in data.iloc[:, :2].values:
            print("Phone number not found")
            self.enter_status = False
            return
        self.enter_status = True

    def statistics(self):
        # outgoing calls number
        outgoings_number = data["caller"].value_counts()[self.phone_number]
        # average time of outgoing accepted calls
        outgoings_average = data[(data.caller == self.phone_number) & (data.duration > 0)].duration.mean()
        # incoming calls number
        incoming_number = data["recipient"].value_counts()[self.phone_number]
        # average time of incoming accepted calls
        incoming_average = data[(data.recipient == self.phone_number) & (data.duration > 0)].duration.mean()
        # number of missed incoming calls
        missed = data[(data.recipient == self.phone_number) & (data.duration == -2)].duration.count()
        # number of rejected incoming calls
        rejected = data[(data.recipient == self.phone_number) & (data.duration == -1)].duration.count()
        if outgoings_number > 0:
            print(f"{outgoings_number} accepted outgoing call(s), average time: {outgoings_average // 60}"
                  f" min {outgoings_average % 60} sec")
        else:
            print("No accepted outgoing calls were found")
        if incoming_number > 0:
            print(f"{incoming_number} accepted incoming call(s), average time: {incoming_average // 60}"
                  f" min {incoming_average % 60} sec")
        else:
            print("No accepted incoming calls were found")
        print(f"{missed} missed call(s)")
        print(f"{rejected} rejected call(s)")

    def history(self, user):
        print(f"Call history with {user}")
        history = ""
        outgoing = data[(data.caller == self.phone_number) & (data.recipient == user)]
        incoming = data[(data.caller == user) & (data.recipient == self.phone_number)]
        history_table = pd.concat([outgoing, incoming], ignore_index=True)
        if len(history_table) == 0:
            history = "Calls history is empty"
        else:
            for i in range(len(history_table)):
                if history_table.iloc[i, 0] == self.phone_number:
                    # outgoing call
                    history += f"Out: {history_table.loc[i, 'dt']} - {history_table.loc[i, 'duration'] // 60} min " \
                           f"{history_table.loc[i, 'duration'] % 60} sec\n"
                elif history_table.iloc[i, 0] == user:
                    # incoming call
                    history += f"In: {history_table.loc[i, 'dt']} - "
                    if history_table.loc[i, 'duration'] == -1:
                        # rejected call
                        history += "rejected\n"
                    elif history_table.loc[i, 'duration'] == -2:
                        # missed call
                        history += "missed\n"
                    else:
                        # regular call
                        history += f"{history_table.loc[i, 'duration'] // 60} min " \
                                   f"{history_table.loc[i, 'duration'] % 60} sec\n"
        print(history)
        f = open(fr"src\call_history\{self.phone_number}-{user}.txt", "w")
        f.write(history)
