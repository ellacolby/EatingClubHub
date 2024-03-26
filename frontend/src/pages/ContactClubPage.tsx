import ClubContacts from "../components/ContactClub/ClubContacts";

const ContactClubPage = () => {
  return (
    <div>
      <a href="/">Back Home</a>
      <h1>Contact the Officers</h1>
      <hr></hr>
      <ClubContacts club={"Cottage"} />
      <ClubContacts club={"Ivy"} />
      <ClubContacts club={"Charter"} />
      <ClubContacts club={"Cap and Gown"} />
    </div>
  );
};

export default ContactClubPage;
