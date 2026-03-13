export const RegistrationRequestConfirmation = () => {
  return (
    <>
      <Box sx={{ mb: 2 }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, color: "text.primary", mb: 0.5 }}>
          {tournament.title}
        </Typography>
        <Chip
          label={gameName}
          size="small"
          icon={<SportsEsportsIcon sx={{ fontSize: 14 }} />}
          sx={{
            backgroundColor: "action.hover",
            fontWeight: 500,
            fontSize: "0.75rem",
          }}
        />
      </Box>

      <Box
        sx={{
          p: 2,
          borderRadius: 2,
          backgroundColor: "action.hover",
          mb: 2,
        }}
      >
        <Box sx={{ display: "flex", justifyContent: "space-between", mb: 1 }}>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Дата начала
          </Typography>
          <Typography variant="body2" sx={{ fontWeight: 600, color: "text.primary" }}>
            {formatDate(tournament.start_at)}
          </Typography>
        </Box>
        <Box sx={{ display: "flex", justifyContent: "space-between" }}>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Участников
          </Typography>
          <Typography variant="body2" sx={{ fontWeight: 600, color: "text.primary" }}>
            {tournament.participants_count} / {tournament.max_participants}
          </Typography>
        </Box>
      </Box>

      <Typography variant="body2" sx={{ color: "text.secondary", lineHeight: 1.6 }}>
        Вы собираетесь подать заявку на участие в турнире. После подтверждения организатор рассмотрит вашу заявку.
      </Typography>
    </>
  );
};
