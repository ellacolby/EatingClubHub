const ClubContact = ({ club }: { club: string }) => {
  return (
    <div>
      <h2>Club: {club}</h2>
      <strong>President: Cynthia Nwankwo</strong>
      <p>Email: cynthia@princeton.edu</p>
      <strong>Vice President: Peter Anella</strong>
      <p>Email: peter@princeton.edu</p>
    </div>
  );
};

export default ClubContact;
