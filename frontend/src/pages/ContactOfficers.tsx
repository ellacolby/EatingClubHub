import ClubContact from "../components/ContactOfficers/ClubContact";

const ContactOfficers = () => {
  return (
    <div>
      <a href="/">Back Home</a>
      <h1>Contact the Officers</h1>
      <hr></hr>
      <ClubContact club={"Cottage"} />
      <ClubContact club={"Ivy"} />
      <ClubContact club={"Charter"} />
      <ClubContact club={"Cap and Gown"} />
    </div>
  );
};

export default ContactOfficers;
