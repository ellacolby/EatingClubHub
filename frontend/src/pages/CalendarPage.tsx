import "../styles/CalendarPage.css";
import ToggleSwitch from "../components/CalendarPage/ToggleSwitch";

const Sidebar = () => {
  const Date = () => {
    return (
      <p className="date month">
        April <span className="date year">2023</span> &lt; &gt;
      </p>
    );
  };

  const EatingClubs = () => {
    return <h3 id="eating-club-header">Eating Clubs</h3>;
  };
  return (
    <div className="sidebar">
      <Date />
      <EatingClubs />
      <div className="toggles-row">
        <ToggleSwitch label={"Cloister"} />
        <ToggleSwitch label={"Cannon"} />
      </div>
      <div className="toggles-row">
        <ToggleSwitch label={"Cottage"} />
        <ToggleSwitch label={"Ivy"} />
      </div>
    </div>
  );
};

const Calendar = () => {
  return (
    <table className="calendar">
      <thead>
        <tr>
          <td></td>
          <td>Sunday</td>
          <td>Monday</td>
          <td>Tuesday</td>
          <td>Wednesday</td>
          <td>Thursday</td>
          <td>Friday</td>
          <td>Saturday</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>7 AM</td>
        </tr>
        <tr>
          <td>8 AM</td>
        </tr>
        <tr>
          <td>9 AM</td>
        </tr>
        <tr>
          <td>10 AM</td>
        </tr>
        <tr>
          <td>11 AM</td>
        </tr>
        <tr>
          <td>12 PM</td>
        </tr>
        <tr>
          <td>1 PM</td>
        </tr>
        <tr>
          <td>2 PM</td>
        </tr>
        <tr>
          <td>3 PM</td>
        </tr>
        <tr>
          <td>4 PM</td>
        </tr>
        <tr>
          <td>5 PM</td>
        </tr>
      </tbody>
    </table>
  );
};

const CalendarPage = () => {
  return (
    <div className="calendar-page">
      <Sidebar />
      <Calendar />
    </div>
  );
};

export default CalendarPage;
