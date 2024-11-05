{ pkgs }: {
  deps = [
    pkgs.glibcLocales
    pkgs.flow-cli  # Correct Flow CLI for the blockchain
  ];
}