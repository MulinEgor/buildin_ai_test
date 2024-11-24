/*
  Warnings:

  - Changed the type of `candles` on the `analized_candles` table. No cast exists, the column would be dropped and recreated, which cannot be done if there is data, since the column is required.

*/
-- AlterTable
ALTER TABLE "analized_candles" DROP COLUMN "candles",
ADD COLUMN     "candles" JSONB NOT NULL;
